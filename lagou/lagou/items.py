# -*- coding: utf-8 -*-

import scrapy
from collections import OrderedDict


LagouInfo = OrderedDict([
    (u'职位', 'name'),
    (u'详细', 'detail'),
    (u'薪资', 'salary'),
    (u'公司', 'company'),
    (u'经验', 'experience'),
    (u'地址', 'address'),
    (u'优势', 'advantage'),
    (u'描述', 'description'),
    (u'学历', 'education'),
    (u'时间', 'time'),
    (u'标签', 'flags'),
    (u'领域', 'field'),
    (u'阶段', 'trend'),
    (u'规模', '1'),
    (u'主页', 'home'),
])


class LagouItem(scrapy.Item):
    name = scrapy.Field()
    salary = scrapy.Field()
    company = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()
    address = scrapy.Field()
    advantage = scrapy.Field()
    description = scrapy.Field()
    detail = scrapy.Field()
    time = scrapy.Field()
    flags = scrapy.Field()
    field = scrapy.Field()
    trend = scrapy.Field()
    scale = scrapy.Field()
    home = scrapy.Field()