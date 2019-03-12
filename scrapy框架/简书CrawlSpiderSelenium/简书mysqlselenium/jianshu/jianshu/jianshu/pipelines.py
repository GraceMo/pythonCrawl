# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.exporters import JsonLinesItemExporter


# class JianshuPipeline(object):
#     def __init__(self):
#         self.i = 1
#     #     self.f = open('jianshu.json','ab')
#     #     self.operater = JsonLinesItemExporter(self.f,encoding='utf8',ensure_ascii=False)
#     def process_item(self, item, spider):
#         self.i += 1
#         print('大概个数有:', self.i)
#         with open('jianshu.json', 'a', encoding='utf8') as f:
#             f.write(json.dumps(dict(item), ensure_ascii=False, indent=4))
import pymysql

class JianshuPipeline(object):
    def __init__(self):
        self.i = 0
        dbparams = {
            'host':'localhost',
            'port':3306,
            'user':'root',
            'password':'123456',
            'charset':'utf8',
            'database':'jianshu'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None
    def process_item(self,item,spider):

        self.cursor.execute(self.sql,(item['title'],item['author'],item['url'],item['content']))
        self.conn.commit()
        self.i += 1
        print(self.i)
        return item
    @property
    def sql(self):
        if not self._sql:
            self._sql = '''
            insert into js(title,author,url,content) values(%s,%s,%s,%s)
            '''
            return self._sql
        return self._sql

