# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib import request
from scrapy.pipelines.images import ImagesPipeline
from bwm.settings import IMAGES_STORE


class BwmPipeline(object):
    def __init__(self):
        self.image_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'image')
        if not os.path.exists(self.image_file):
            os.mkdir(self.image_file)

    def process_item(self, item, spider):
        category = item['category']
        urls = item['urls']
        category_path = os.path.join(self.image_file, category)
        if not os.path.exists(category_path):
            os.mkdir(category_path)
        for url in urls:
            img_name = url.split('_')[-1]
            request.urlretrieve(url, os.path.join(category_path, img_name))
        return item


class BwmImsPipline(ImagesPipeline):  # # todo 5
    def get_media_requests(self, item, info):
        request_objs = super(BwmImsPipline, self).get_media_requests(item, info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None):
        path = super(BwmImsPipline, self).file_path(request, response, info)
        image_store = IMAGES_STORE
        category = request.item.get('category')
        category_path = os.path.join(image_store, category)
        if not category_path:
            os.mkdir(category_path)
        image_name = path.replace('full/', '')
        image_path_name = os.path.join(category_path, image_name)
        return image_path_name
