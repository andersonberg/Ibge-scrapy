__author__ = 'andersonberg'

import scrapy
from cnes_scrapy.items import PibScrapyItem


class PibSpider(scrapy.Spider):
    name = "pib"
    allowed_domains = ["pt.wikipedia.org"]
    start_urls = ["http://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_de_Pernambuco_por_PIB_per_capita"]

    def parse(self, response):
        import ipdb ; ipdb.set_trace()
        table = response.xpath('//table[@class="wikitable sortable"]')
        for table_row in table.xpath('.//tr'):
            pib = table_row.xpath('.//td').re_first(r'\d{1,3}\s+\d{1,3}\s+\d{1,3}')
            if pib:
                print("PIB: %s" % pib)
            cidade = table_row.xpath('.//td/a/text()').extract_first()
            if cidade:
                print("Cidade: %s" % cidade)
