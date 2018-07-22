# -*- coding: utf-8 -*-

import re
import scrapy
from datetime import datetime
from scrapy.spiders import Spider
from faker import Factory
from urllib.parse import urlparse, parse_qs
from scrapy.http import Request
from ..items import DoubanItem

x_page = r'//dl[@class="obu"]/dt/a/@href'
x_location = r'//div[@class="user-info"]/a/text()'
x_nick_name = r'//div[@class="info"]/h1/text()'
x_user_name = r'//div[@class="user-info"]/div[@class="pl"]/text()'

f = Factory.create()


class FansSpider(Spider):
    name = 'fans'
    allowed_domains = ['accounts.douban.com', 'douban.com']
    start_urls = [
        'https://www.douban.com/'
    ]
    custom_settings = {
        'ITEM_PIPELINES': {
            'douban.pipelines.DoubanCsvPipeline': 100
        }
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Host': 'accounts.douban.com',
        'User-Agent': f.user_agent()
    }

    formdata = {
        'form_email': 'xxxx',
        'form_password': 'xxxxx',
        # 'captcha-solution': '',
        # 'captcha-id': '',
        'login': '登录',
        'redir': 'https://www.douban.com/',
        'source': 'None'
    }

    def __init__(self):
        super(FansSpider, self).__init__()
        self.base_url = 'https://www.douban.com'
        self.start_url = 'https://www.douban.com/people/guokr42/rev_contacts'

        print(u'########## [START] Start Maizi Spider, Time: %s ##########' % datetime.now())

    def start_requests(self):
        return [scrapy.Request(url='https://www.douban.com/accounts/login',
                               headers=self.headers,
                               meta={'cookiejar': 1},
                               callback=self.parse_login)]

    def parse_login(self, response):
        if b'captcha_image' in response.body:
            print('Copy the link:')
            link = response.xpath('//img[@class="captcha_image"]/@src').extract()[0]
            print(link)
            captcha_solution = input('captcha-solution:')
            captcha_id = parse_qs(urlparse(link).query, True)['id']
            self.formdata['captcha-solution'] = captcha_solution
            self.formdata['captcha-id'] = captcha_id

        return [scrapy.FormRequest.from_response(response,
                                                 formdata=self.formdata,
                                                 headers=self.headers,
                                                 meta={'cookiejar': response.meta['cookiejar']},
                                                 callback=self.after_login
                                                 )]

    def after_login(self, response):
        self.headers['Host'] = "www.douban.com"
        yield scrapy.Request('https://www.douban.com/people/guokr42/rev_contacts',
                             meta={'cookiejar': response.meta['cookiejar']},
                             headers=self.headers,
                             callback=self.parse_paginator)

    def parse_paginator(self, response):
        for paginator in range(482):
            yield Request('%s?start=%d' % (self.start_url, paginator * 70), self.parse_page,
                          headers=self.headers, meta={'cookiejar': response.meta['cookiejar']})

    def parse_page(self, response):
        for sel in response.xpath(x_page):
            yield Request(sel.extract(), self.parse_detail,
                          headers=self.headers, meta={'cookiejar': response.meta['cookiejar']})

    def parse_detail(self, response):
        try:
            location = response.xpath(x_location).extract()[0].strip()
        except IndexError:
            location = ''

        if '成都' in location:
            item = DoubanItem()
            item['nick_name'] = response.xpath(x_nick_name).extract()[0].strip()
            item['user_name'] = response.xpath(x_user_name).extract()[0].strip()
            item['url'] = response.url
            yield item
        else:
            return
