# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class GushiwenPipeline(object):
    def __init__(self):
        client = MongoClient(host='192.168.3.31',port=27017)
        self.collection = client['GuShiWen']['poem']
    def process_item(self, item, spider):
        print(item)
        self.collection.insert(item)
        print('------')

        return item
