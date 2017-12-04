# -*- coding: utf-8 -*-

from openpyxl import Workbook
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

from .items import LagouInfo


class LagouPipeline(object):
    def open_spider(self, spider):
        self.wb = Workbook()
        self.wb.create_sheet()
        self.wb.active.title = u'%s-%s' % (spider.city, spider.language)

        ws = self.wb[self.wb.active.title]
        ws.append(LagouInfo.keys())


    def close_spider(self, spider):
        self.wb.remove_sheet(self.wb.get_sheet_by_name('Sheet1'))
        self.wb.save('lagou.xlsx')

    def process_item(self, item, spider):
        self.wb[self.wb.active.title].append([item.get(v, '') for v in LagouInfo.values()])
        return item
