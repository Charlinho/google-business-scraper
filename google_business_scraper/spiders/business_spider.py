import scrapy
from google_business_scraper.items import BusinessItem
import urllib.parse
import json

class BusinessSpider(scrapy.Spider):
    name = 'business'
    allowed_domains = ['google.com']

    def __init__(self, search_query=None, max_results=50, *args, **kwargs):
        super(BusinessSpider, self).__init__(*args, **kwargs)

        # Usar parâmetro passado ou valor padrão
        self.search_query = search_query or "salão de beleza atibaia"
        self.max_results = int(max_results)

        self.start_urls = [
            f'https://www.google.com/search?q={urllib.parse.quote(self.search_query)}&tbm=lcl'
        ]

        self.logger.info(f"Configurado para buscar: {self.search_query}")
        self.logger.info(f"Máximo de resultados: {self.max_results}")

    def start_requests(self):
        for url in self.start_urls:
            self.logger.info(f"Iniciando busca: {url}")
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
                    'Accept-Encoding': 'gzip, deflate',  # Remover br (brotli) temporariamente
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                },
                meta={'dont_cache': True}
            )

    def parse(self, response):
        self.logger.info(f"Processando página: {response.url}")
        self.logger.info(f"Status da resposta: {response.status}")
        self.logger.info(f"Tipo de conteúdo: {response.headers.get('content-type', b'').decode()}")

        # Verificar se o conteúdo é texto
        try:
            content_type = response.headers.get('content-type', b'').decode().lower()
            if 'text/html' not in content_type:
                self.logger.warning(f"Tipo de conteúdo inesperado: {content_type}")

            # Tentar decodificar o conteúdo
            if hasattr(response, 'text'):
                html_content = response.text
                self.logger.info(f"Conteúdo HTML obtido - tamanho: {len(html_content)} caracteres")
            else:
                self.logger.error("Não foi possível obter o conteúdo HTML")
                return

        except Exception as e:
            self.logger.error(f"Erro ao processar resposta: {e}")
            # Salvar conteúdo bruto para debug
            with open('debug_raw_response.html', 'wb') as f:
                f.write(response.body)
            return

        # Seletores para diferentes layouts do Google
        business_selectors = [
            'div[data-cid]',  # Seletor principal
            '.VkpGBb',        # Seletor alternativo
            '.rllt__details', # Outro seletor
            'div.VkpGBb',     # Variação
            '.g',             # Seletor genérico do Google
            '[data-ved]',     # Elementos com data-ved
        ]

        businesses_found = False
        items_count = 0

        # Salvar HTML para debug
        with open('debug_page.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        self.logger.info("HTML da página salvo em debug_page.html")

        for selector in business_selectors:
            try:
                businesses = response.css(selector)
                if businesses:
                    self.logger.info(f"Encontrados {len(businesses)} elementos com seletor: {selector}")
                    businesses_found = True

                    for i, business in enumerate(businesses[:self.max_results]):
                        self.logger.info(f"Processando elemento {i+1}/{len(businesses)}")
                        item = self.extract_business_data(business, response, selector)
                        if item:
                            items_count += 1
                            yield item

                            if items_count >= self.max_results:
                                self.logger.info(f"Limite de {self.max_results} resultados atingido")
                                break
                    break
            except Exception as e:
                self.logger.error(f"Erro ao processar seletor {selector}: {e}")
                continue

        if not businesses_found:
            self.logger.warning("Nenhum negócio encontrado com os seletores disponíveis")
            # Tentar extrair qualquer texto que pareça ser nome de negócio
            items_count = self.try_alternative_extraction(response)

        self.logger.info(f"Total de itens extraídos: {items_count}")

    def extract_business_data(self, business, response, used_selector):
        try:
            # Log do HTML do elemento para debug
            element_html = business.get()
            self.logger.debug(f"HTML do elemento (primeiros 200 chars): {element_html[:200]}...")

            # Extrair nome - múltiplas tentativas
            name_selectors = [
                '.OSrXXb::text',
                'h3::text',
                '.BNeawe.vvjwJb.AP7Wnd::text',
                '.LC20lb.MBeuO.DKV0Md::text',
                'a h3::text',
                '.r a h3::text',
                'h3.LC20lb::text',
                '.yuRUbf h3::text',
            ]

            name = None
            for selector in name_selectors:
                try:
                    name = business.css(selector).get()
                    if name and name.strip():
                        self.logger.info(f"Nome encontrado com seletor '{selector}': {name}")
                        break
                except:
                    continue

            # Se não encontrou nome, tentar extrair qualquer texto
            if not name:
                all_texts = business.css('::text').getall()
                for text in all_texts:
                    if text and len(text.strip()) > 3 and not text.strip().isdigit():
                        name = text.strip()
                        self.logger.info(f"Nome extraído de texto geral: {name}")
                        break

            if not name:
                self.logger.warning(f"Nenhum nome encontrado para elemento com seletor {used_selector}")
                return None

            # Extrair outros dados com tentativas múltiplas
            rating_selectors = [
                '.BTtC6e::text',
                'span.yi40Hd.YrbPuc::text',
                '.AJLUJb::text',
                '.fTKmHE99XE4__star-rating::text',
            ]

            rating = None
            for selector in rating_selectors:
                try:
                    rating = business.css(selector).get()
                    if rating:
                        break
                except:
                    continue

            # Extrair número de avaliações
            review_selectors = [
                '.RDApEe.YrbPuc::text',
                'span.RDApEe::text',
                '.YrbPuc::text',
            ]

            review_count = None
            for selector in review_selectors:
                try:
                    review_count = business.css(selector).get()
                    if review_count and '(' in review_count:
                        review_count = review_count.strip('()')
                        break
                except:
                    continue

            # Extrair localização
            location_selectors = [
                '.UaQhfb::text',
                '.rllt__details .UaQhfb::text',
                '.VkpGBb .UaQhfb::text',
            ]

            location = None
            for selector in location_selectors:
                try:
                    location = business.css(selector).get()
                    if location:
                        break
                except:
                    continue

            # Criar item
            item = BusinessItem()
            item['name'] = name.strip() if name else ''
            item['rating'] = rating.strip() if rating else ''
            item['review_count'] = review_count.strip() if review_count else ''
            item['location'] = location.strip() if location else ''
            item['category'] = self.search_query.split()[0].title()
            item['url'] = ''

            self.logger.info(f"Item criado: {item['name']}")
            return item

        except Exception as e:
            self.logger.error(f"Erro ao extrair dados do negócio: {e}")
            return None

    def try_alternative_extraction(self, response):
        """Método alternativo para tentar extrair dados quando os seletores principais falham"""
        self.logger.info("Tentando extração alternativa...")
        items_count = 0

        try:
            # Procurar por qualquer texto que pareça ser nome de negócio
            potential_names = response.css('h3::text, .BNeawe::text, .OSrXXb::text, a::text').getall()

            # Filtrar nomes válidos
            valid_names = []
            for name in potential_names:
                if (name and 
                    len(name.strip()) > 3 and 
                    not name.strip().isdigit() and
                    'Google' not in name and
                    'Maps' not in name):
                    valid_names.append(name.strip())

            self.logger.info(f"Encontrados {len(valid_names)} nomes potenciais")

            for name in valid_names[:min(10, self.max_results)]:
                item = BusinessItem()
                item['name'] = name
                item['rating'] = ''
                item['review_count'] = ''
                item['location'] = ''
                item['category'] = self.search_query.split()[0].title()
                item['url'] = ''

                self.logger.info(f"Item alternativo extraído: {item['name']}")
                items_count += 1
                yield item

        except Exception as e:
            self.logger.error(f"Erro na extração alternativa: {e}")

        return items_count
