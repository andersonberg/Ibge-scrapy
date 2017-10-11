# -*- coding: utf-8 -*-

# Scrapy settings for cnes_scrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'cnes_scrapy'

SPIDER_MODULES = ['cnes_scrapy.spiders']
NEWSPIDER_MODULE = 'cnes_scrapy.spiders'

ITEM_PIPELINES = {
   'cnes_scrapy.pipelines.CnesScrapyPipeline': 300,
}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'cnes_scrapy (+http://www.yourdomain.com)'

DOWNLOAD_DELAY = 2

# MONGO_URI = 'localhost:27017'
# MONGO_DATABASE = 'cnes'
MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "cnes"
MONGODB_COLLECTION = "equipamentos"