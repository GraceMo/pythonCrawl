# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouse(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    rooms = scrapy.Field()
    area = scrapy.Field()
    address = scrapy.Field()
    district = scrapy.Field()
    sale = scrapy.Field()
    price = scrapy.Field()
    origin_url = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()

class EsfHouse(scrapy.Item):
    name = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    rooms = scrapy.Field()
    floor = scrapy.Field()
    toward = scrapy.Field()
    year = scrapy.Field()
    address = scrapy.Field()
    area = scrapy.Field()
    price = scrapy.Field()
    unit = scrapy.Field()
    origin_url = scrapy.Field()