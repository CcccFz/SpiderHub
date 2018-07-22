# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    nick_name = scrapy.Field()
    user_name = scrapy.Field()
    url = scrapy.Field()
