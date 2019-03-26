# -*- coding: utf-8 -*-
import scrapy
import re
from DD.items import DdItem
class DangdSpider(scrapy.Spider):
    name = 'dangd'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://category.dangdang.com/pg1-cp01.03.56.00.00.00.html']
    url = 'http://category.dangdang.com/pg{}-cp01.03.56.00.00.00.html'
    i = 1
    def parse(self, response):
        li_list = response.xpath("//div[@id='search_nature_rg']//li")
        for li in li_list:
            name = li.xpath("./a/@title").get()
            price = li.xpath(".//p[@class='price']/span[1]/text()").get()
            url = li.xpath("./a/@href").get()
            author = li.xpath(".//p[@class='search_book_author']//a[1]/@title").get()
            item = DdItem(
                name=name,
                author=author,
                price=price,
                url=url
            )
            yield item
        while self.i <=99:
            self.i += 1
            url = self.url.format(self.i)
            yield scrapy.Request(url=url,callback=self.parse)