# -*- coding: utf-8 -*-

import ConfigParser
from scrapy.spiders import Spider
from scrapy.http import Request
from ..items import LagouItem


HEADERS = {
    'Host': 'www.lagou.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'user_trace_token=20171018161110-e6697698-b3db-11e7-9bbc-525400f775ce; LGUID=20171018161110-e6697983-b3db-11e7-9bbc-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F%3Fmsg%3Dvalidation%26uStatus%3D3%26clientIp%3D118.122.117.66; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=17; TG-TRACK-CODE=index_navigation; index_location_city=%E6%88%90%E9%83%BD; login=false; unick=""; _putrc=""; JSESSIONID=ABAAABAACDBABJB64EBBDC23CD306A6E77829E51B84A022; _gat=1; SEARCH_ID=1b77c59d97b244dd994d0bc5492cbb25; X_HTTP_TOKEN=fabff1161fd65aba6e1807e755b49129; _gid=GA1.2.930088128.1512357398; _ga=GA1.2.319510511.1508314246; LGSID=20171204143024-9c336045-d8bc-11e7-9c02-5254005c3644; LGRID=20171204145003-5b19c95f-d8bf-11e7-8262-525400f775ce; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1512019528,1512090911,1512111055,1512361538; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1512370204'
}

x_last_page = '//div[@class="pager_container"]/a[last()-1]/text()'
x_items = '//li[@class="con_list_item default_list"]'
x_item_link = './/a[@class="position_link"]/@href'
x_name = '//span[@class="name"]/text()'
x_salary = '//span[@class="salary"]/text()'
x_company = '//dl[@class="job_company"]/dt/a/img/@alt'
x_experience = '//dd/p/span[3]/text()'
x_education = '//dd/p/span[4]/text()'
x_advantage = '//dd[@class="job-advantage"]/p/text()'
x_description = '//dd[@class="job_bt"]/div/node()'
x_address = '//div[@class="work_addr"]/a/text()'
x_time = '//p[@class="publish_time"]/text()'
x_flags = '//ul[starts-with(@class, "position-label")]/li[@class="labels"]/text()'
x_company_info = '//dl[@class="job_company"]/dd/ul[@class="c_feature"]/li/text()'
x_home = '//dl[@class="job_company"]/dd/ul[@class="c_feature"]/li/a/@href'


class CaseConfigParser(ConfigParser.ConfigParser):
    def __init__(self):
        ConfigParser.ConfigParser.__init__(self)

    def optionxform(self, optionstr):
        return optionstr


class LagouSpider(Spider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'lagou.pipelines.LagouPipeline': 100,
        }
    }

    def __init__(self):
        super(LagouSpider, self).__init__()
        config = CaseConfigParser()
        config.read('scrapy.cfg')
        self.city = config.get('filter', 'city').decode('utf-8')
        self.language = config.get('filter', 'language').decode('utf-8')
        self.base_url = 'https://www.lagou.com/zhaopin/Python'

    def start_requests(self):
        yield Request(self.base_url, self.parse_paginator, headers=HEADERS)

    def parse_paginator(self, response):
        last = int(response.xpath(x_last_page).extract()[0])
        for i in xrange(1, last+1):
            yield Request('%s/%d' % (self.base_url, i), self.parse_item, headers=HEADERS)

    def parse_item(self, response):
        for sel_item in response.xpath(x_items):
            detail = sel_item.xpath(x_item_link).extract()[0]
            yield Request(detail, self.parse_detail, headers=HEADERS)

    def parse_detail(self, response):
        item = LagouItem()
        item['detail'] = response.url
        item['name'] = response.xpath(x_name).extract()[0]
        item['salary'] = response.xpath(x_salary).extract()[0]
        item['company'] = response.xpath(x_company).extract()[0]
        item['experience'] = response.xpath(x_experience).extract()[0]
        item['address'] = '-'.join(response.xpath(x_address).extract())
        item['advantage'] = response.xpath(x_advantage).extract()[0]
        item['description'] = ''.join(response.xpath(x_description).extract())
        item['education'] = response.xpath(x_education).extract()[0]
        item['time'] = response.xpath(x_time).extract()[0]
        item['flags'] = ','.join(response.xpath(x_flags).extract())
        item['home'] = response.xpath(x_home).extract()[0]
        item['field'], item['trend'], item['scale'] = [x for x in response.xpath(x_company_info).extract() if not x.startswith('\n')]
        yield item
