# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import os
import requests
from datetime import datetime
from scrapy.exceptions import DropItem


def test(item):
    print '--------------------------------'
    print item['suit']
    print item['course']
    print item['name']
    print item['name_en']
    print item['url']


def download_video(base_path, item):
    path = os.path.join(base_path, item['suit'], item['course'])
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, u'%s.mp4' % item['name']), 'wb') as wf:
        wf.write(requests.get(item['url']).content)


class BatchvideoPipeline(object):

    def __init__(self):
        self._path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'videos')
        self._count = 0

    def open_spider(self, spider):
        if not os.path.exists(self._path):
            os.mkdir(self._path)

    def close_spider(self, spider):
        print u'#################################################### [END] End Maizi Spider, Time: %s, Total: %d ####################################################' \
              % (datetime.now(), self._count)

    def process_item(self, item, spider):
        if item['suit'] and item['course'] and item['name'] and item['url']:
            self._count += 1
            # download_video(self._path, item)
            test(item)
            return item
        else:
            raise DropItem(u'[Error] Not find mp4 in this site: %s%s' % (spider.base_url, item['name_en']))
