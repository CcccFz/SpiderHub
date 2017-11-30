# -*- coding: utf-8 -*-


import logging
from scrapy.spiders import Spider
from scrapy.http import Request
from fang.items import AnjukeItem, AnjukeInfo

class AnjukeSpider(Spider):
    name = "anjuke"
    custom_settings = {
        'ITEM_PIPELINES': {
            'fang.pipelines.PdAnjukePipeline': 100,
            'fang.pipelines.AnjukePipeline': 200,
            'fang.pipelines.AnjukeImagesPipeline': 300,
        }
    }
    allowed_domains = ["anjuke.com"]
    base_url = 'https://cd.fang.anjuke.com/loupan/'
    sections = [u'成华', u'双流', u'高新', u'新都', u'温江', u'龙泉驿',
                u'郫都', u'锦江', u'武侯', u'青羊', u'金牛', u'高新西区',
                u'都江堰', u'青白江', u'新津', u'成都周边', u'大邑', u'蒲江',
                u'金堂', u'彭州', u'邛崃', u'崇州', u'天府新区']

    def __init__(self):
        self._callbacks = {}
        for k, v in AnjukeInfo.iteritems():
            self._callbacks[k] = getattr(self, v, self.default_callback)

    def start_requests(self):
        yield Request(self.base_url, self.parse)

    def parse(self, response):
        for sel in response.xpath('//div[@class="item-list area-bd"]/div[@class="filter"]/a'):
            loc = sel.xpath('text()').extract()[0].strip()
            if loc in self.sections:
                url = sel.xpath('@href').extract()[0]
                for i in xrange(1, 10):
                    url = '%sp%d/' % (url, i)
                    yield Request(url, self.parse_page, meta={'loc': loc})

    def parse_page(self, response):
        for url in response.xpath('//div[@class="item-mod"]/@data-link').extract():
            yield Request(url.replace(self.base_url, 'https://cd.fang.anjuke.com/loupan/canshu-'),
                          callback=self.parse_detail,
                          meta={'loc': response.meta['loc']})

    def parse_detail(self, response):
        item = AnjukeItem()
        item['loc'] = response.meta['loc']
        url = None
        for sel in response.xpath('//div[@class="can-border"]/ul/li/div[@class="name"]'):
            attr = sel.xpath('text()').extract()[0]
            if attr in AnjukeInfo:
                if attr == u'参考单价':
                    url = sel.xpath('../div[@class="des"]/a/@href').extract()
                    url = url[0] if url else None
                field = AnjukeInfo[attr]
                value = self._callbacks[attr](sel.xpath('../div[@class="des"]'))
                item[field] = value if isinstance(value, int) else ''.join(value.split()).strip()

        if url:
            yield Request(url, callback=self.parse_item, meta={'item': item})
        else:
            yield item

    def parse_item(self, response):
        item = response.meta['item']
        sel = response.xpath('//div[@class="pL glb_xp"]/div[@class="ld3"]/img/@src')
        if sel:
            item['image_urls'] = sel.extract()[0]
        yield item

    def default_callback(self, sel):
        return sel.xpath('text()').extract()[0]

    def building_name(self, sel):
        return sel.xpath('a/text()').extract()[0]

    def building_feature(self, sel):
        return u'、'.join(sel.xpath('a[@soj="canshu_left_tips"]/text()').extract())

    def refer_price(self, sel):
        price = sel.xpath('span[@class="can-spe can-big space2"]/text()')
        if price :
            try:
                return int(price.extract()[0])
            except ValueError:
                return int(price.extract()[0].split('-')[-1])
        else:
            return 0

    def developers(self, sel):
        devper = sel.xpath('a/text()')
        if not devper:
            return sel.xpath('text()').extract()[0]
        return devper.extract()[0]

    def regional_position(self, sel):
        first = sel.xpath('text()').extract()[0]
        last = '-'.join(sel.xpath('a[@soj="canshu_left_quyu"]/text()').extract())
        return '%s%s' % (first, last)

    def house_type(self, sel):
        return u'、'.join(sel.xpath('a[@soj="canshu_left_huxing"]/text()').extract())

