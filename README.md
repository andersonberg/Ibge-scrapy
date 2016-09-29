# Ibge-scrapy

[![Coverage Status](https://coveralls.io/repos/github/andersonberg/Ibge-scrapy/badge.svg?branch=master)](https://coveralls.io/github/andersonberg/Ibge-scrapy?branch=master)
[![Build Status](https://travis-ci.org/andersonberg/Ibge-scrapy.svg?branch=master)](https://travis-ci.org/andersonberg/Ibge-scrapy)

This script synthesise GDP (PIB in portuguese) data, total population ([IBGE](http://www.ibge.gov.br/) data), medical assist lifes ([ANS](http://www.ans.gov.br/) data) and all hospital equipments ([CNES](http://cnes.datasus.gov.br) data) in cities from brazilian northeast region.

## Usage
Call the main script:
    $python cobertura/cobertura_nordeste.py
It will generate an excel file named "Cobertura NE.xls"

## Tests
To run the tests, just do:
    $python setup.py tests
