# -*- coding: utf-8 -*-

from collections import OrderedDict
import scrapy


AnjukeInfo = OrderedDict([
    (u'¥������', 'building_name'),
    (u'¥���ص�', 'building_feature'),
    (u'�ο�����', 'refer_price'),
    (u'��ҵ����', 'property_type'),
    (u'������'  , 'developers'),
    (u'����λ��', 'regional_position'),
    (u'¥�̵�ַ', 'residential_address'),
    (u'����׸�', 'initial_payment'),
    (u'�¹�'    , 'monthly_payment'),
    (u'¥���Ż�', 'privilege'),
    (u'¥�̻���', 'house_type'),
    (u'����ʱ��', 'open_time'),
    (u'����ʱ��', 'completion_date'),
    (u'��¥����ַ', 'sale_address'),
    (u'��������', 'building_type'),
    (u'��Ȩ����', 'property_year'),
    (u'�ݻ���'  , 'volume_rate'),
    (u'�̻���'  , 'green_rate'),
    (u'�滮����', 'plan_number'),
    (u'¥��״��', 'floor_condition'),
    (u'���̽���', 'progress_work'),
    (u'��ҵ�����', 'manage_fee'),
    (u'��ҵ��˾', 'manage_company'),
    (u'��λ��'  , 'parking_number'),
    (u'��λ��'  , 'parking_ratio'),
    (u'�۸�����', 'price_trend'),
    (u'¥��ͼƬ', 'building_images'),
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

    # ���ڴ�������
    loc = scrapy.Field()    # ��ʾ����

    # ����ͼƬ�ܵ�
    image_urls = scrapy.Field()
    image_names = scrapy.Field()

