# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PibScrapyItem(scrapy.Item):
    cidade = scrapy.Field()
    pib = scrapy.Field()


class CnesScrapyItem(scrapy.Item):
    cidade = scrapy.Field()
    equipamento = scrapy.Field()
    existentes = scrapy.Field()
    emUso = scrapy.Field()
    existentesSUS = scrapy.Field()
    emUsoSUS = scrapy.Field()
