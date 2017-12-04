# -*- coding: utf-8 -*-

import ConfigParser
from scrapy.spiders import Spider
from scrapy.http import Request
from ..items import LagouItem


# HEADERS = {
#     'Host': 'www.lagou.com',
#     'Connection': 'keep-alive',
#     'Cache-Control': 'max-age=0',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3253.3 Safari/537.36',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Cookie': 'ga=GA1.2.1004716071.1509266707; user_trace_token=20171029164508-780667eb-bc85-11e7-9651-5254005c3644; LGUID=20171029164508-78066ab2-bc85-11e7-9651-5254005c3644; index_location_city=%E6%88%90%E9%83%BD; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=17; JSESSIONID=ABAAABAAAIAACBI204663A37DF71D0E73C158F96F1EC4F9; _gid=GA1.2.1808661989.1512187800; _putrc=BF511E86B2FB54D9; login=true; unick=%E5%88%98%E6%99%93%E5%B8%86; _gat=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1511602145,1512187800,1512195179,1512195183; LGSID=20171202141323-e715a45a-d727-11e7-9b8f-5254005c3644; PRE_UTM=m_cf_cpc_baidu_pc; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Fbaidu.php%3Fsc.Kf0000K3JnppHiJ7Wpy4EjQZCXOFY82rzHD_xM21526pOaCHIkqapJNkWWlLH5o0Vx6fXigjDeKGdYWaBjhE3OwyWqQm1ETjtJHZU2h9E2DC7UGjH67eMEZi8YpvAxd0JaN2P90zrD7PFOD2rPdsn45vK-SEucIRwDzmVKHFNepshAAwSf.DR_NR2Ar5Od663rj6tJQrGvKD7ZZKNfYYmcgpIQC8xxKfYt_U_DY2yP5Qjo4mTT5QX1BsT8rZoG4XL6mEukmryZZjzsLTJplePXO-8zNqrw5Q9tSMj_qTr1x9tqvZul3xg1sSxW9qx-9LdoDkEvyN4QPh1-LTVvGmuCyrreGoz20.U1Yk0ZDqs2v4VnL30ZKGm1Yk0Zfqs2v4VnL30A-V5HczPfKM5gN-rH00Iybqmh7GuZN_UfKspyfqnW60mv-b5HczP6KVIjYknjD4g1DsnHIxnH0zndt1njDdg1nvnjD0pvbqn0KzIjYknHn0uy-b5HDYnWNxnHbsn1NxnWDsP1-xnWRkP160mhbqnW0Y0AdW5Hm3rjDsnjfsn7tvrj6vnHb4rjIxnNtknjFxn0KkTA-b5H00TyPGujYs0ZFMIA7M5H00mycqn7ts0ANzu1Ys0ZKs5HR4PWDYP1bznsK8IM0qna3snj0snj0sn0KVIZ0qn0KbuAqs5H00ThCqn0KbugmqTAn0uMfqn0KspjYs0Aq15H00mMTqnH00UMfqn0K1XWY0IZN15Hnkn1fknHT4P1DvPHR1PW61P100ThNkIjYkPHDznHbdnHbvPHD30ZPGujd-nWTLnHP-P10snjPbmhm40AP1UHd7rRRsf1IjrjcYn16LfHmk0A7W5HD0TA3qn0KkUgfqn0KkUgnqn0KlIjYs0AdWgvuzUvYqn7tsg1Kxn7ts0Aw9UMNBuNqsUA78pyw15HKxn7tsg1nkrjm4nNts0ZK9I7qhUA7M5H00uAPGujYzPW6Yn1RYPHm0ugwGujYVnfK9TLKWm1Ys0ZNspy4Wm1Ys0Z7VuWYs0AuWIgfqn0KhXh6qn0Khmgfqn0KlTAkdT1Ys0A7buhk9u1Yk0Akhm1Ys0APzm1Y1PHbkPs%26ck%3D7585.3.95.238.267.358.308.305%26shh%3Dwww.baidu.com%26sht%3D98012088_5_dg%26us%3D1.0.2.0.1.493.0%26ie%3Dutf-8%26f%3D8%26ch%3D11%26tn%3D98012088_5_dg%26wd%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%26oq%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%26rqlang%3Dcn%26euri%3D8982940%26bc%3D110101; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flp%2Fhtml%2Fcommon.html%3Futm_source%3Dm_cf_cpc_baidu_pc%26m_kw%3Dbaidu_cpc_cd_e110f9_d2162e_%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591; LGRID=20171202141328-e9d09e02-d727-11e7-9b8f-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1512195188',
# }

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
x_item = '//li[@class="con_list_item default_list"]'
x_item_name = '@data-positionname'
x_item_salary = '@data-salary'
x_item_company = '@data-company'
x_item_link = './/a[@class="position_link"]/@href'
x_detail_head = ''


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
        for sel_item in response.xpath(x_item):
            detail = sel_item.xpath(x_item_link).extract()[0]
            yield Request(detail, self.parse_detail, headers=HEADERS)

    def parse_detail(self, response):
        item = LagouItem()
        item['name'] = '1'
        item['salary'] = '1'
        item['company'] = '1'
        item['detail'] = response.url
        yield item
