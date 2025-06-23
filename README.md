# 🤖 Google Business Scraper

Um scraper Python robusto para extrair informações de negócios do Google usando Scrapy. Extrai dados como nome, avaliação, número de reviews, localização e categoria de empresas.

## 📋 Funcionalidades

- ✅ Busca automática no Google por negócios locais
- ✅ Extração de dados estruturados (nome, avaliação, reviews, localização)
- ✅ Exportação automática para Excel (.xlsx)
- ✅ Rotação de User-Agents para evitar bloqueios
- ✅ Sistema de retry e throttling inteligente
- ✅ Logs detalhados e sistema de debug
- ✅ Suporte a múltiplos seletores CSS
- ✅ Tratamento robusto de erros

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **Scrapy** - Framework de web scraping
- **OpenPyXL** - Manipulação de arquivos Excel
- **Fake-UserAgent** - Rotação de user agents
- **Brotli** - Suporte a compressão

## 📦 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/Charlinho/google-business-scraper.git
cd google-business-scraper-scrapy
```

### 2. Crie um ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt

### 4. Verifique a instalação
```bash
scrapy version
```

## 🚀 Como Usar

### Comando Básico
```bash
python3 run_scraper.py --search "salão de beleza atibaia" --max-results 50
```

### Exemplos de Uso

#### Buscar restaurantes italianos em São Paulo
```bash
python3 run_scraper.py --search "restaurante italiano são paulo" --max-results 100
```

#### Buscar academias no Rio de Janeiro
```bash
python3 run_scraper.py --search "academia rio de janeiro" --max-results 75
```

#### Buscar clínicas veterinárias em Belo Horizonte
```bash
python3 run_scraper.py --search "clínica veterinária belo horizonte" --max-results 30
```

### Parâmetros Disponíveis

| Parâmetro | Descrição | Exemplo | Padrão |
|-----------|-----------|---------|---------|
| `--search` | Termo de busca | `"salão de beleza atibaia"` | `"salão de beleza atibaia"` |
| `--max-results` | Número máximo de resultados | `100` | `50` |

## 📁 Estrutura do Projeto

```
google-business-scraper-scrapy/
├── google_business_scraper/
│   ├── __init__.py
│   ├── items.py              # Definição dos itens de dados
│   ├── middlewares.py        # Middleware personalizado
│   ├── pipelines.py          # Pipeline de processamento
│   ├── settings.py           # Configurações do Scrapy
│   └── spiders/
│       ├── __init__.py
│       └── business_spider.py # Spider principal
├── data/                     # Arquivos Excel gerados
├── debug_page.html          # HTML de debug (gerado automaticamente)
├── requirements.txt         # Dependências básicas
├── requirements_with_brotli.txt # Dependências com suporte Brotli
├── run_scraper.py          # Script principal de execução
├── test_pipeline.py        # Script de teste
└── README.md              # Este arquivo
```

## 📊 Dados Extraídos

O scraper extrai as seguintes informações para cada negócio:

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| **Nome** | Nome do estabelecimento | "Salão Beleza & Estilo" |
| **Avaliação** | Nota média (0-5 estrelas) | "4.5" |
| **Número de Avaliações** | Quantidade de reviews | "127" |
| **Localização** | Endereço ou bairro | "Centro, Atibaia - SP" |
| **Categoria** | Tipo de negócio | "Salão" |
| **URL** | Link (quando disponível) | "https://..." |

## 📈 Arquivo de Saída

Os dados são salvos automaticamente em:
```
data/[termo_da_busca].xlsx
```

**Exemplo:**
- Busca: `"restaurante italiano são paulo"`
- Arquivo: `data/restaurante_italiano_são_paulo.xlsx`

## ⚙️ Configurações Avançadas

### Modificar Configurações do Scrapy

Edite o arquivo `google_business_scraper/settings.py`:

```python
# Delay entre requisições (segundos)
DOWNLOAD_DELAY = 2

# Número máximo de requisições simultâneas
CONCURRENT_REQUESTS = 1

# Ativar AutoThrottle
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
```

### Personalizar User-Agents

O middleware `RotateUserAgentMiddleware` rotaciona automaticamente os user-agents. Para personalizar, edite `middlewares.py`.

## 🐛 Solução de Problemas

### Erro: "cannot decode the response from unsupported encoding 'br'"
```bash
pip install brotli brotlicffi
```

### Erro: "Response content isn't text"
- Verifique sua conexão com a internet
- O Google pode estar bloqueando requisições
- Execute novamente após alguns minutos

### Arquivo Excel vazio
- Verifique os logs para erros de extração
- O arquivo `debug_page.html` será criado para análise
- Tente com um termo de busca diferente

### Spider não encontrado
```bash
# Certifique-se de estar no diretório correto
cd google-business-scraper-scrapy

# Verifique se o spider existe
scrapy list
```

## 📝 Logs e Debug

### Visualizar Logs Detalhados
```bash
python3 run_scraper.py --search "sua busca" --max-results 50 2>&1 | tee scraper.log
```

### Arquivos de Debug Gerados
- `debug_page.html` - HTML da página processada
- `debug_raw_response.html` - Resposta bruta em caso de erro

### Níveis de Log
- `INFO` - Informações gerais
- `WARNING` - Avisos
- `ERROR` - Erros críticos
- `DEBUG` - Informações detalhadas

## 🧪 Testes

### Testar Pipeline
```bash
python3 test_pipeline.py
```

### Testar Spider Diretamente
```bash
cd google_business_scraper
scrapy crawl business -a search_query="teste" -a max_results=5
```

## 🔧 Desenvolvimento

### Adicionar Novos Seletores CSS

Edite `business_spider.py` e adicione novos seletores no array `business_selectors`:

```python
business_selectors = [
    'div[data-cid]',
    '.VkpGBb',
    '.rllt__details',
    '.seu-novo-seletor',  # Adicione aqui
]
```

### Modificar Campos Extraídos

Edite `items.py` para adicionar novos campos:

```python
class BusinessItem(scrapy.Item):
    name = scrapy.Field()
    rating = scrapy.Field()
    # Adicione novos campos aqui
    phone = scrapy.Field()
    website = scrapy.Field()
```

## 📋 Requisitos do Sistema

- **Python**: 3.8 ou superior
- **Sistema Operacional**: Windows, macOS, Linux
- **Memória RAM**: Mínimo 512MB
- **Espaço em Disco**: 100MB para instalação + espaço para dados

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## ⚠️ Aviso Legal

Este scraper é destinado apenas para fins educacionais e de pesquisa. Certifique-se de:

- Respeitar os Termos de Serviço do Google
- Não fazer requisições excessivas
- Usar os dados de forma ética e legal
- Considerar implementar delays maiores para uso em produção
