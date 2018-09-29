# -*- coding: utf-8 -*-

import re
from .utils import convert
import datetime
import configparser
from scrapy.spiders import Spider
from scrapy.http import Request
from ..items import JobItem


HEADERS = {
    'Host': 'www.lagou.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'JSESSIONID=ABAAABAAADEAAFI932ED1A8B743DC62CE4C735C8986AF1A; _ga=GA1.2.1309324775.1514274379; user_trace_token=20171226154621-dd9427e2-ea10-11e7-9e89-5254005c3644; LGUID=20171226154621-dd942d24-ea10-11e7-9e89-5254005c3644; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1514274382; X_HTTP_TOKEN=736731781cacb029cffe097b474db4c4; _putrc=BF511E86B2FB54D9; login=true; unick=%E5%88%98%E6%99%93%E5%B8%86; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=17; index_location_city=%E6%88%90%E9%83%BD; TG-TRACK-CODE=index_navigation; _gid=GA1.2.760638227.1514451922; SEARCH_ID=2487edbecaa14c83a896843c3c4f90ed; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1514515993; LGSID=20171229105320-6d86b262-ec43-11e7-9f67-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2FPython%2F; LGRID=20171229105320-6d86b509-ec43-11e7-9f67-5254005c3644'
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
x_zone = '//div[@class="work_addr"]/a/text()'
x_address = '//div[@class="work_addr"]/text()'
x_time = '//p[@class="publish_time"]/text()'
x_flag = '//ul[starts-with(@class, "position-label")]/li[@class="labels"]/text()'
x_company_info = '//dl[@class="job_company"]/dd/ul[@class="c_feature"]/li/text()'
x_home = '//dl[@class="job_company"]/dd/ul[@class="c_feature"]/li/a/@href'
quote_pattern = re.compile(r'[s\n,，\+]+')
rmcls_pattern = re.compile(r'class=\".*?\"')


class CaseConfigParser(configparser.ConfigParser):
    def __init__(self):
        configparser.ConfigParser.__init__(self)

    def optionxform(self, optionstr):
        return optionstr


class LagouSpider(Spider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            # 'job.pipelines.WbPipeline': 100,
            'job.pipelines.MongoPipeline': 200,
        }
    }

    def __init__(self):
        super(LagouSpider, self).__init__()
        config = CaseConfigParser()
        config.read('scrapy.cfg')
        self.city = config.get('filter', 'city')
        self.language = config.get('filter', 'language')
        self.base_url = 'https://www.lagou.com/zhaopin/Python'
        self.t = datetime.datetime.now()

    def start_requests(self):
        yield Request(self.base_url, self.parse_paginator, headers=HEADERS)

    def parse_paginator(self, response):
        last = int(response.xpath(x_last_page).extract()[0])
        for i in range(1, last+1):
            yield Request('%s/%d' % (self.base_url, i), self.parse_item, headers=HEADERS)

    def parse_item(self, response):
        for sel_item in response.xpath(x_items):
            detail = sel_item.xpath(x_item_link).extract()[0]
            yield Request(detail, self.parse_detail, headers=HEADERS)

    def parse_detail(self, response):
        item = JobItem()
        item['detail'] = response.url
        item['name'] = response.xpath(x_name).extract()[0]
        item['salary'] = response.xpath(x_salary).extract()[0].strip()
        item['salary_min'], item['salary_max'] = list(map(lambda y: int(y[:-1]), item['salary'].split('-')))
        item['company'] = response.xpath(x_company).extract()[0].replace('有限责任公司', '').replace('股份有限公司', '').replace('有限公司', '')

        item['experience'] = response.xpath(x_experience).extract()[0].replace('经验', '').split()[0]
        if '-' in item['experience']:
            item['experience_min'] = list(map(int, item['experience'][:-1].split('-')))[0]
        else:
            if item['experience'] == '不限':
                item['experience_min'] = 0
            else:
                item['experience_min'] = 0.5

        try:
            item['zone'] = response.xpath(x_zone).extract()[-2]
            item['address'] = '%s-%s-%s' % (self.city, item['zone'], response.xpath(x_address).extract()[-2].split()[-1])
        except IndexError:
            item['zone'] = self.city
            item['address'] = '%s-%s' % (item['zone'], response.xpath(x_address).extract()[0])
        item['coordinate'] = convert(item['address'])

        item['benefit'] = '<br>'.join(quote_pattern.split(response.xpath(x_advantage).extract()[0]))
        item['description'] = ''.join(response.xpath(x_description).extract()).replace('\n', '').strip()
        item['description'] = rmcls_pattern.sub('', item['description'])
        item['education'] = response.xpath(x_education).extract()[0].replace('及以上', '').split()[0]
        item['time'] = response.xpath(x_time).extract()[0].split()[0]
        if '-' in item['time']:
            item['actual_time'] = datetime.datetime.strptime(item['time'], '%Y-%m-%d')
        elif ':' in item['time']:
            time_str = '%s %s' % (self.t.strftime('%Y-%m-%d'), item['time'])
            item['actual_time'] = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M')
        else:
            item['actual_time'] = self.t - datetime.timedelta(days=int(item['time'][0]))

        item['flag'] = '<br>'.join(quote_pattern.split(','.join(response.xpath(x_flag).extract())))
        item['home'] = response.xpath(x_home).extract()[0]
        item['field'], item['trend'], item['scale'] = [x.strip() for x in response.xpath(x_company_info).extract() if not x.startswith('\n')]
        item['field'] = '<br>'.join(quote_pattern.split(item['field']))

        if '-' in item['scale']:
            item['scale_max'] = int(item['scale'][:-1].split('-')[-1])
        else:
            if '以上' in item['scale']:
                item['scale_max'] = 5000
            else:
                item['scale_max'] = 15

        yield item
