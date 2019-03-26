# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter

import pymysql
class JingdongPipeline(object):
    # def __init__(self):
    #     self.f = open('jdbook.json', 'wb')
    #     self.exporter = JsonLinesItemExporter(self.f,encoding='utf8', ensure_ascii=False, indent=4)
    #
    # def process_item(self, item, spider):
    #     self.exporter.export_item(item)
    #     return item
    #
    # def close_spider(self,spider):
    #     self.f.close()
    MYSQL_HOST = '192.168.3.20'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_PORT = 3306
    MYSQL_DBNAME = 'jd_book'
    MYSQL_CHARSET = 'utf8'
    def __init__(self):
        self.conn = pymysql.connect(host=self.MYSQL_HOST,
                                    port=self.MYSQL_PORT,
                                    db=self.MYSQL_DBNAME,
                                    user=self.MYSQL_USER,
                                    passwd=self.MYSQL_PASSWORD,
                                    charset=self.MYSQL_CHARSET,)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        self.cursor.execute('insert into book(Bsort,Ssort,name,author,price,url) values(%s,%s,%s,%s,%s,%s)',[
            item['big_sort'],
            item['small_sort'],
            item['book_name'],
            item['author'],
            item['price'],
            item['url'],
        ])
        self.conn.commit()
    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()
