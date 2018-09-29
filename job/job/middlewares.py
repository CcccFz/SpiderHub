# -*- coding: utf-8 -*-

import random
import requests
from scrapy import signals
from . import useragents
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware      # UserAegent中间件
from scrapy.downloadermiddlewares.retry import RetryMiddleware


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").content


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def get_useful_proxy():
    while True:
        proxy = get_proxy()
        try:
            ret = requests.get('http://www.lagou.com', proxies={'http': 'http://%s' % proxy}, timeout=5)
            if ret.status_code == 200:
                return proxy
            else:
                delete_proxy(proxy)
                continue
        except Exception:
            delete_proxy(proxy)
            continue


class JobSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RotateUserAgentMiddleware(UserAgentMiddleware):

    def process_request(self, request, spider):
        agent = random.choice(useragents.agents)
        request.headers.setdefault(b'User-Agent', agent)        


class CookieMiddleware(RetryMiddleware):

    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def process_request(self, request, spider):
        cook = random.choice(useragents.cookies)
        request.cookies = {'user_trace_token': cook}


class ProxyMiddleware(object):

    def process_request(self, request, spider):
        request.meta['proxy'] = "http://%s" % get_useful_proxy()


class RotateUserAgentMiddleware(UserAgentMiddleware):

    def process_request(self, request, spider):
        agent = random.choice(useragents.agents)
        request.headers.setdefault(b'User-Agent', agent)


