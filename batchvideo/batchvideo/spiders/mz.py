# -*- coding: utf-8 -*-

import re
from datetime import datetime
from scrapy.spiders import Spider
from scrapy.http import Request
from ..items import BatchvideoItem


r_paginator = r'/course/%s/0-\d+/'
r_course = re.compile(r'<a title="(.*)" href="(/course/(\d+)/)">')
r_url = re.compile(r'http://.*maizi.*\.mp4')
x_name = r'//span[@class="fl"]'



class MaiziSpider(Spider):
    name = 'maizi'
    allowed_domains = ['www.maiziedu.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'batchvideo.pipelines.BatchvideoPipeline': 100,
        }
    }

    def __init__(self):
        super(MaiziSpider, self).__init__()
        self.base_url = 'http://www.maiziedu.com'
        self.start_url = 'http://www.maiziedu.com/course/%s/0-1/'
        self.need_suits = {
        	# 'python-all': u'python web开发'
            # 'web-all': u'web前端开发',
            'te-all': '软件测试'
            # 'sec-all': u'网络安全',
            # 'oam-all': u'自动化运维',
            # 'java-all': u'java开发',
            # 'ml-all': u'机器学习'
        }
        print(u'########## [START] Start Maizi Spider, Time: %s ##########' % datetime.now())

    def start_requests(self):
        for suit_en, suit_cn in self.need_suits.items():
            yield Request(self.start_url % suit_en, self.parse_paginator,
                          meta={'suit_cn': u'%s' % suit_cn, 'suit_en': u'%s' % suit_en})

    def parse_paginator(self, response):
        for paginator in re.findall(r_paginator % response.meta['suit_en'], response.text):
            print(paginator)
            yield Request(u'%s%s' % (self.base_url, paginator), self.parse_page, meta=response.meta)

    def parse_page(self, response):
        repeat_list = []
        for course_cn, course_en, course_id in r_course.findall(response.text):            
            if course_cn in repeat_list:
                continue
            repeat_list.append(course_cn)            
            response.meta['course_cn'], response.meta['course_id'] = course_cn, course_id
            yield Request(u'%s%s' % (self.base_url, course_en), self.parse_detail, meta=response.meta)

    def parse_detail(self, response):
        for sel in response.xpath(x_name):
            name_en = sel.xpath(r'../@href').extract()[0]
            response.meta['name_cn'], response.meta['name_en'] = sel.xpath(r'text()').extract()[0], name_en
            if 'course' not in name_en:
                continue
            yield Request(u'%s%s' % (self.base_url, name_en), self.parse_item, meta=response.meta)

    def parse_item(self, response):
        item = BatchvideoItem()
        item['suit'] = response.meta['suit_cn'].strip()
        item['course'] = response.meta['course_cn'].strip()        
        item['name'] = response.meta['name_cn'].strip()
        item['name_en'] = response.meta['name_en'].strip()
        try:
            item['url'] = r_url.search(response.text).group().strip()
        except AttributeError:
            item['url'] = None
        yield item
