# -*- coding: utf-8 -*-

import scrapy


class LolItem(scrapy.Item):
    name = scrapy.Field()
    urls = scrapy.Field()

