# -*- coding: utf-8 -*-

from openpyxl import Workbook
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

from .items import JobInfo


class WbPipeline(object):
    def open_spider(self, spider):
        self.wb = Workbook()
        self.wb.create_sheet()
        self.wb.active.title = '%s-%s' % (spider.city, spider.language)

        ws = self.wb[self.wb.active.title]
        ws.append(JobInfo.keys())

    def close_spider(self, spider):
        self.wb.remove_sheet(self.wb.get_sheet_by_name('Sheet1'))
        self.wb.save('lagou.xlsx')

    def process_item(self, item, spider):
        self.wb[self.wb.active.title].append([item.get(v, '') for v in JobInfo.values()])
        return item


class MongoPipeline(object):
    def open_spider(self, spider):
        self.client = MongoClient('mongodb://127.0.0.1:27017/')
        self.db = self.client.jobs
        self.db.lagou.drop()
        self.col = self.db.lagou

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.col.insert({k: v for k, v in item.items()})
        return item
