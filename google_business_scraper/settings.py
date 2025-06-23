# Scrapy settings for google_business_scraper project

BOT_NAME = 'google_business_scraper'

SPIDER_MODULES = ['google_business_scraper.spiders']
NEWSPIDER_MODULE = 'google_business_scraper.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure delays for requests
RANDOMIZE_DOWNLOAD_DELAY = 0.5
DOWNLOAD_DELAY = 2
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# Configure pipelines
ITEM_PIPELINES = {
    'google_business_scraper.pipelines.ValidationPipeline': 300,
    'google_business_scraper.pipelines.ExcelExportPipeline': 400,
}

# Configure middlewares
DOWNLOADER_MIDDLEWARES = {
    'google_business_scraper.middlewares.RotateUserAgentMiddleware': 400,
}

# Default headers
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Configure concurrent requests
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1

# Configure cookies
COOKIES_ENABLED = True

# Configure retry settings
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# Log level
LOG_LEVEL = 'INFO'
