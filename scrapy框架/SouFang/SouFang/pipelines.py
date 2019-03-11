# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter
class NewHousePipeline(object):
    def __init__(self):
        self.f1 = open('newfang.json','wb')
        self.f2 = open('esffang.json','wb')
        self.operator1 = JsonLinesItemExporter(self.f1,ensure_ascii=False,indent=4,encoding='utf8')
        self.operator2= JsonLinesItemExporter(self.f2,ensure_ascii=False,indent=4,encoding='utf8')
    def process_item(self, item, spider):

        self.operator1.export_item(item)
        self.operator2.export_item(item)
        return item
    def close_spider(self,item,spider):
        self.f.close()
