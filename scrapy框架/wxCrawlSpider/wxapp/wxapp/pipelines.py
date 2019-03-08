# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter


class WxappPipeline(object):
    def open_spider(self, spider):
        self.f = open('wxapp.json', 'wb')
        self.exporter = JsonLinesItemExporter(self.f, ensure_ascii=False, encoding='utf8', indent=4)

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.f.close()
