# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter


class SunyuPipeline(object):
    def __init__(self):
        self.f = open('sun.json', 'a b')
        self.operator = JsonLinesItemExporter(self.f, encoding='utf8', ensure_ascii=False)

    def process_item(self, item, spider):
        print('******-----item--------*******')
        self.operator.export_item(item)
        return item

    def close_spider(self,spider):
        self.f.close()
