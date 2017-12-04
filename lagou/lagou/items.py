# -*- coding: utf-8 -*-

import scrapy
from collections import OrderedDict


LagouInfo = OrderedDict([
    (u'岗位名', 'name'),
    (u'公司', 'company'),
    (u'薪资', 'salary'),
    # (u'经验'  , 'developers'),
    # (u'地址', 'residential_address'),
    # (u'福利', 'initial_payment'),
    # (u'描述', 'monthly_payment'),
    (u'详细', 'detail'),
])


class LagouItem(scrapy.Item):
    name = scrapy.Field()
    salary = scrapy.Field()
    company = scrapy.Field()
    experience = scrapy.Field()
    city = scrapy.Field()
    address = scrapy.Field()
    advantage = scrapy.Field()
    description = scrapy.Field()
    detail = scrapy.Field()

