# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from openpyxl import Workbook
from scrapy.exceptions import DropItem


class DoubanXlsxPipeline(object):

    def __init__(self):
        self.wb = None

    def open_spider(self, spider):
        self.wb = Workbook()
        self.wb.create_sheet()
        self.wb.active.title = '关注果壳网的人（成都）'
        ws = self.wb[self.wb.active.title]
        ws.append(['用户名', '昵称', '个人主页'])

    def close_spider(self, spider):
        self.wb.remove_sheet(self.wb.get_sheet_by_name('Sheet1'))
        self.wb.save('关注果壳网的人.xlsx')

    def process_item(self, item, spider):
        self.wb[self.wb.active.title].append([item['user_name'], item['nick_name'], item['url']])
        return item


class DoubanCsvPipeline(object):

    total = 0

    def __init__(self):
        self._file = None

    def open_spider(self, spider):
        self._file = open('关注果壳网的人.csv', 'w')
        self._file.write('用户名,昵称,个人主页\n')

    def close_spider(self, spider):
        self._file.close()
        print('******************* 总数为：%s ********************' % self.total)

    def process_item(self, item, spider):
        self.total += 1
        if '成都' in item['location']:
            self._file.write('%s,%s,%s\n' % (item['user_name'], item['nick_name'], item['url']))
            return item
        else:
            raise DropItem('Not in ChengDU')
