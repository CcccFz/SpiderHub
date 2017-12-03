# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import LolItem

x_name = '//h1[@class="hero-name"]/text()'
x_urls = '//li[starts-with(@class, "ui-slide__panel")]/img/@src'

class LolSpider(CrawlSpider):
    name = "lol"
    custom_settings = {
        'ITEM_PIPELINES': {
            'lol.pipelines.LolImagesPipeline': 100,
        }
    }
    allowed_domains = ['lol.duowan.com']
    base_url = 'http://lol.duowan.com/hero'
    start_urls = ['http://lol.duowan.com/hero']
    rules = (
        Rule(LinkExtractor(allow=('^http://lol.duowan.com/[a-z]+/$')),
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = LolItem(urls=[])
        item['urls'].extend(response.xpath(x_urls).extract())
        try:
            item['name'] = response.xpath(x_name).extract()[0]
        except IndexError:
            return
        yield item
