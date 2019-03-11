# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter
class NewHousePipeline(object):
    def __init__(self):
        self.f = open('fang.json','wb')
        self.operator = JsonLinesItemExporter(self.f,ensure_ascii=False,indent=4,encoding='utf8')
    def process_item(self, item, spider):
        self.operator.export_item(item)
        return item
    def close_spider(self,item,spider):
        self.f.close()
