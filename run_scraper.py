#!/usr/bin/env python3
"""
Script para executar o Google Business Scraper com parâmetros personalizados
"""

import argparse
import sys
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    parser = argparse.ArgumentParser(description='Google Business Scraper')
    parser.add_argument('--search', '-s', required=True, 
                       help='Termo de busca (ex: "salão de beleza atibaia")')
    parser.add_argument('--max-results', '-m', type=int, default=50,
                       help='Número máximo de resultados (padrão: 50)')
    parser.add_argument('--output', '-o', 
                       help='Nome do arquivo de saída (sem extensão)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Modo verboso (mais logs)')

    args = parser.parse_args()

    print(f"🚀 Iniciando scraper...")
    print(f"📍 Busca: {args.search}")
    print(f"📊 Max resultados: {args.max_results}")

    try:
        # Configurar settings
        settings = get_project_settings()

        if args.verbose:
            settings.set('LOG_LEVEL', 'DEBUG')
        else:
            settings.set('LOG_LEVEL', 'INFO')

        # Configurar nome do arquivo de saída
        if args.output:
            output_filename = f"{args.output}.xlsx"
        else:
            # Criar nome baseado na busca
            safe_search = args.search.replace(' ', '_').replace(',', '').lower()
            output_filename = f"{safe_search}.xlsx"

        settings.set('EXCEL_FILENAME', output_filename)

        # Executar o crawler
        process = CrawlerProcess(settings)

        # O nome do spider é 'business' (definido no business_spider.py)
        process.crawl('business', 
                     search_query=args.search,
                     max_results=args.max_results)

        process.start()

        print(f"✅ Scraping concluído!")
        print(f"📁 Arquivo salvo: data/{output_filename}")

    except Exception as e:
        print(f"❌ Erro durante execução:")
        print(str(e))
        sys.exit(1)

if __name__ == '__main__':
    main()
