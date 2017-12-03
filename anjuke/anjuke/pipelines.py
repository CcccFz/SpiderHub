# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import logging
from collections import OrderedDict

from openpyxl import Workbook
import pandas as pd
import charts

from fang.items import AnjukeInfo
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request



class AnjukePipeline(object):
    def open_spider(self, spider):
        self.wb = Workbook()
        for idx, loc in enumerate(spider.sections):
            if idx:
                self.wb.create_sheet(loc)
            else:
                self.wb.active.title = loc
            ws = self.wb[loc]

            ws.append(AnjukeInfo.keys())

            for num in xrange(65, 65 + len(AnjukeInfo)):
                if num > 90:
                    coordinate = 'A%s' % chr(num - 26)
                else:
                    coordinate = chr(num)
                ws.column_dimensions[coordinate].width = 15.0

    def close_spider(self, spider):
        self.wb.save('anjuke.xlsx')

    def process_item(self, item, spider):
        if item['loc'] in self.wb:
            values = [item[field] if field in item else '' for field in AnjukeInfo.values()]
            self.wb[item['loc']].append(values)
            return item
        else:
            logging.error('No exists the sheet[%s] in excel' % item['loc'])
            #  raise DropItem("miss item %s" % item)

class PdAnjukePipeline(object):
    def open_spider(self, spider):
        self.data = OrderedDict(zip(spider.sections,
                                    [OrderedDict() for x in spider.sections]
                                )
                    )

    def close_spider(self, spider):
        writer = pd.ExcelWriter('anjuke_pd.xlsx')
        charts_data = {'avg': []}
        for loc, loc_data in self.data.iteritems():
            df = pd.DataFrame(loc_data)
            df.to_excel(writer, sheet_name=loc, index=False)

            charts_data[loc] = zip(loc_data[u'楼盘名称'], loc_data[u'参考单价'])
            tmp = [x for x in loc_data[u'参考单价'] if x]
            charts_data['avg'].append({'name': loc, 'data': [sum(tmp)/len(tmp)], 'type': 'column'})

        charts.plot(charts_data['avg'], show='inline', save='avg.html',
                    options={'title': {'text': u'区域新房均价'}})
        charts.plot([{'name': x, 'data': charts_data[x]} for x in charts_data if x != 'avg'],
                    show='inline', save='anjuke.html',
                    options={'title': {'text': u'成都所有新房'}})
        writer.save()

    def process_item(self, item, spider):
        if item['loc'] in self.data:
            for attr, field in AnjukeInfo.iteritems():
                if attr not in self.data[item['loc']]:
                    self.data[item['loc']][attr] = [item[field] if field in item else '']
                else:
                    self.data[item['loc']][attr].append(item[field] if field in item else '')
            return item
        else:
            logging.error('No exists the sheet[%s] in excel' % item['loc'])
            #  raise DropItem("miss item %s" % item)

class AnjukeImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        return u'%s/00_价格趋势图.jpg' % request.meta['dir']

    def get_media_requests(self, item, info):
        if 'image_urls' in item:
            yield Request('https://%s' % item['image_urls'],
                          meta={'dir': item['building_name']})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        #  if not image_paths:
            #  raise DropItem("Item contains no images %s" % item['building_name'])
        return item
