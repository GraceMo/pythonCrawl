# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter


class BossPipeline(object):
    def __init__(self):
        self.f = open('boss.json', 'wb')
        self.exporter = JsonLinesItemExporter(self.f, ensure_ascii=False, indent=4, encoding='utf8')

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        print('---')
        return item

    def close_spider(self, spider):
        self.f.close()
