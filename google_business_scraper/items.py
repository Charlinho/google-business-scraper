import scrapy

class BusinessItem(scrapy.Item):
    # Definir todos os campos que serão usados
    name = scrapy.Field()
    rating = scrapy.Field()
    review_count = scrapy.Field()
    location = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
