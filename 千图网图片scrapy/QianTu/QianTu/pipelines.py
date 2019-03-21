# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from urllib.request import urlretrieve
import os,random
class QiantuPipeline(object):
    def process_item(self, item, spider):
        mid = item['title']
        # i = 0
        # src_list = item['src']
        cont = item['src']
        name = '.\\quw\\%s' % mid + '.jpg'
        if os.path.exists(name):
            num = random.choice(range(99))
            name = '.\\quw\\%s' % mid +str(num)+ '.jpg'
        with open(name,'wb')as f:
            f.write(cont)
            # urlretrieve(url=url,filename=name)
        print('---sucess--')
        return item
