# -*- coding: utf-8 -*-
__author__ = 'anderson'

import re
import scrapy
import pandas as pd
from siemens_scrapy.items import CnesScrapyItem


class CnesSpider(scrapy.Spider):
    name = "cnes"
    allowed_domains = ["cnes.datasus.gov.br"]
    start_urls = []

    def __init__(self):
        codigos_cidades = self.get_cities()
        for cidade in codigos_cidades:
            codigo_estado = self.get_state_code(cidade)
            self.start_urls.append("http://cnes.datasus.gov.br/Mod_Ind_Equipamento.asp?VEstado=%s&VMun=%s" % (codigo_estado, cidade))

    def parse(self, response):
        table = response.xpath('//table[@border="1"]')
        for sel in table.xpath('.//tr'):
            line = sel.xpath('td/font/text()').extract()
            equipamento = sel.xpath('td/font/a/text()').extract()
            cidade = self.get_city_from_url(response.url)

            # Preenche o item com os dados extraídos
            item = CnesScrapyItem()
            item['cidade'] = cidade

            if len(line) > 0 and len(equipamento) > 0:
                existentes = line[-4]
                emUso = line[-3]
                existentesSUS = line[-2]
                emUsoSUS = line[-1]

                item['equipamento'] = equipamento[0]
                item['existentes'] = existentes
                item['emUso'] = emUso
                item['existentesSUS'] = existentesSUS
                item['emUsoSUS'] = emUsoSUS

                yield item

    def get_cities(self):
        codigos_cidades = []
        filename = "ANS Vidas Assistidas NE.xls"
        data = pd.read_excel(filename, parse_cols=0)
        for line in data.values:
            for cidade in line:
                cod_cidade = re.match(r'[\d]+', cidade)
                if cod_cidade:
                    codigos_cidades.append(cod_cidade.group())

        return codigos_cidades

    def get_state_code(self, cod_cidade):
        state_code = cod_cidade[0:2]
        return state_code

    def get_city_from_url(self, url):
        cod_cidade = re.match(r"[\w|\W]+VMun=(\d+)$", url)
        if cod_cidade:
            return cod_cidade.group(1)
        else:
            return url
