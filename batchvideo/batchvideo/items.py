# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BatchvideoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    suit = scrapy.Field()
    course = scrapy.Field()
    name = scrapy.Field()
    name_en = scrapy.Field()
    url = scrapy.Field()
