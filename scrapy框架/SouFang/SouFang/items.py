# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseItem(scrapy.Item):
    # define the fields for your item here like:
    house_name = scrapy.Field()
    address = scrapy.Field()
    district = scrapy.Field()
    house_type = scrapy.Field()
    area = scrapy.Field()
    price = scrapy.Field()
    house_url = scrapy.Field()
    labels = scrapy.Field()
    onsale = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()

class EsfItem(scrapy.Item):
    # define the fields for your item here like:
    house_name = scrapy.Field()
    address = scrapy.Field()
    district = scrapy.Field()
    house_type = scrapy.Field()
    area = scrapy.Field()
    price = scrapy.Field()
    house_url = scrapy.Field()
    labels = scrapy.Field()
    onsale = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
