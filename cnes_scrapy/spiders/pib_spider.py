__author__ = 'andersonberg'

import scrapy


class PibSpider(scrapy.Spider):
    name = "pib"
    allowed_domains = ["pt.wikipedia.org"]
    start_urls = ["http://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_de_Pernambuco_por_PIB_per_capita"]

    def parse(self, response):
        table = response.xpath('//table[@class="wikitable sortable"]')
        for sel in table.xpath('.//td'):
            pib = sel.xpath('text()').re(r'\d{1,3}\s+\d{1,3}\s+\d{1,3}')
            if pib:
                print("PIB: %s" % pib[-1])
            cidade = sel.xpath('a/text()').extract()
            if cidade:
                print("Cidade: %s" % cidade[-1])
        # filename = response.url.split("/")[-2]
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
