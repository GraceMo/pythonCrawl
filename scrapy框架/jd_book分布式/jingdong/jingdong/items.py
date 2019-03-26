# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JingdongItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    big_sort = scrapy.Field()
    small_sort = scrapy.Field()
    book_name = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
