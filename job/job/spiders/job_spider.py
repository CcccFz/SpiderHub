# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.http import Request
from ..items import JobItem


x_last_page = '//div[@class="pager_container"]/a[last()-1]/text()'
x_item = '//li[@class="con_list_item default_list"]'
x_item_name = '@data-positionname'
x_item_salary = '@data-salary'
x_item_company = '@data-company'
x_item_link = './/a[@class="position_link"]/@href'
x_detail_head

class JobSpider(Spider):
    name = 'job'
    allowed_domains = ['www.lagou.com']
    base_url = 'https://www.lagou.com/zhaopin/Python'

    custom_settings = {
        'ITEM_PIPELINES': {
            'job.pipelines.JobPipeline': 100,
        }
    }

    def start_requests(self):
        yield Request(self.base_url, self.parse)

    def parse_paginator(self, response):
        last = int(response.xpath(x_last_page)[0])
        for i in xrange(1, last+1):
            yield Request('%s/%d' % (self.base_url, last), self.parse_item)

    def parse_item(self, response):
        for sel_item in response.xpath(x_item):
            print 'name: ', sel_item.xpath(x_item_name)[0]
            print 'salary: ', sel_item.xpath(x_item_salary)[0]
            print 'company: ', sel_item.xpath(x_item_company)[0]
            link = sel_item.xpath(x_item_link)[0]
            print 'link: ', link
            yield Request(link, self.parse_detail)

    def parse_detail(self, response):
        for sel_item in response.xpath(x_item):