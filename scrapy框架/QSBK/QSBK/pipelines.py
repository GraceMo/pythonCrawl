# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonItemExporter


class QsbkPipeline(object):
    def open_spider(self, spider):
        self.f = open('qb.json', 'wb')
        self.exporter = JsonItemExporter(self.f, ensure_ascii=False, encoding='utf8', indent=4)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.f.close()
