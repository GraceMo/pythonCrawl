# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
class DdPipeline(object):
    def __init__(self):
        self.client = MongoClient()
        self.collection = self.client['dangdang']['dd']

    def process_item(self, item, spider):
        self.collection.insert(dict(item))

        return item
