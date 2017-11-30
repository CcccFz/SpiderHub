# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MobaPipeline(object):
    def file_path(self, request, response=None, info=None):
        item, filename = request.meta['item'], request.meta['filename']
        path = u'%s/%s/%s' % (item['name'], item['album'], filename)
        return path

    def get_media_requests(self, item, info):
        for url in item['image_urls']:
            filename = self.get_filename(url)
            yield Request(url, meta={'item': item, 'filename': filename})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
             raise DropItem("Item contains no images")
        return item

    def get_filename(self, url):
        return url[url.rfind('/') + 1:]
