# -*- coding: utf-8 -*-

from collections import OrderedDict
import scrapy


AnjukeInfo = OrderedDict([
    (u'楼盘名称', 'building_name'),
    (u'楼盘特点', 'building_feature'),
    (u'参考单价', 'refer_price'),
    (u'物业类型', 'property_type'),
    (u'开发商'  , 'developers'),
    (u'区域位置', 'regional_position'),
    (u'楼盘地址', 'residential_address'),
    (u'最低首付', 'initial_payment'),
    (u'月供'    , 'monthly_payment'),
    (u'楼盘优惠', 'privilege'),
    (u'楼盘户型', 'house_type'),
    (u'开盘时间', 'open_time'),
    (u'交房时间', 'completion_date'),
    (u'售楼处地址', 'sale_address'),
    (u'建筑类型', 'building_type'),
    (u'产权年限', 'property_year'),
    (u'容积率'  , 'volume_rate'),
    (u'绿化率'  , 'green_rate'),
    (u'规划户数', 'plan_number'),
    (u'楼层状况', 'floor_condition'),
    (u'工程进度', 'progress_work'),
    (u'物业管理费', 'manage_fee'),
    (u'物业公司', 'manage_company'),
    (u'车位数'  , 'parking_number'),
    (u'车位比'  , 'parking_ratio'),
    (u'价格走势', 'price_trend'),
    (u'楼盘图片', 'building_images'),
])

class AnjukeItem(scrapy.Item):
    building_name = scrapy.Field()
    building_feature = scrapy.Field()
    refer_price = scrapy.Field()
    property_type = scrapy.Field()
    developers = scrapy.Field()
    regional_position = scrapy.Field()
    residential_address = scrapy.Field()
    initial_payment = scrapy.Field()
    monthly_payment = scrapy.Field()
    privilege = scrapy.Field()
    house_type = scrapy.Field()
    open_time = scrapy.Field()
    completion_date = scrapy.Field()
    sale_address = scrapy.Field()
    building_type = scrapy.Field()
    property_year = scrapy.Field()
    volume_rate = scrapy.Field()
    green_rate = scrapy.Field()
    plan_number = scrapy.Field()
    floor_condition = scrapy.Field()
    progress_work = scrapy.Field()
    manage_fee = scrapy.Field()
    manage_company = scrapy.Field()
    parking_number = scrapy.Field()
    parking_ratio = scrapy.Field()
    price_trend = scrapy.Field()
    building_images = scrapy.Field()

    # 用于传递数据
    loc = scrapy.Field()    # 表示地域

    # 用于图片管道
    image_urls = scrapy.Field()
    image_names = scrapy.Field()

