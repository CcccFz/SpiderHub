# -*- coding: utf-8 -*-

import scrapy
from collections import OrderedDict


JobInfo = OrderedDict([
    (u'职位', 'name'),
    (u'详细', 'detail'),
    (u'月薪', 'salary'),
    (u'月薪下限', 'salary_min'),
    (u'月薪上限', 'salary_max'),
    (u'公司', 'company'),
    (u'经验', 'experience'),
    (u'经验下限', 'experience_min'),
    (u'区域', 'zone'),
    (u'地址', 'address'),
    (u'坐标', 'coordinate'),
    (u'福利', 'benefit'),
    (u'描述', 'description'),
    (u'学历', 'education'),
    (u'时间', 'time'),
    (u'实际时间', 'actual_time'),
    (u'标签', 'flag'),
    (u'领域', 'field'),
    (u'阶段', 'trend'),
    (u'规模', 'scale'),
    (u'规模上限', 'scale_max'),
    (u'主页', 'home'),
])


class JobItem(scrapy.Item):
    name = scrapy.Field()
    salary = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    company = scrapy.Field()
    experience = scrapy.Field()
    experience_min = scrapy.Field()
    education = scrapy.Field()
    zone = scrapy.Field()
    address = scrapy.Field()
    coordinate = scrapy.Field()
    benefit = scrapy.Field()
    description = scrapy.Field()
    detail = scrapy.Field()
    time = scrapy.Field()
    actual_time = scrapy.Field()
    flag = scrapy.Field()
    field = scrapy.Field()
    trend = scrapy.Field()
    scale = scrapy.Field()
    scale_max = scrapy.Field()
    home = scrapy.Field()
