# -*- coding: utf-8 -*-

import pinyin
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request


class LolImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for url in item['urls']:
            filename = url[url.rfind('/') + 1:]
            yield Request(url, meta={'name': item['name'], 'filename': filename})

    def file_path(self, request, response=None, info=None):
        pyin = lambda x: pinyin.get(x[0], format="numerical")[0].upper()
        name, filename = request.meta['name'], request.meta['filename']
        path = u'%s-%s/%s' % (pyin(name), name, filename)
        return path

    def item_completed(self, results, item, info):
        paths = [ret['path'] for ok, ret in results if ok]
        if not paths:
             raise DropItem("Item contains no images")
        return item
