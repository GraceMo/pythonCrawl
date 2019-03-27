# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jingdong.items import JingdongItem
import re
from scrapy_redis.spiders import RedisCrawlSpider

class DdwSpider(RedisCrawlSpider):
    name = 'ddw'
    allowed_domains = ['dangdang.com']
    # start_urls = ['http://book.dangdang.com']
    redis_key = 'ddw:s'

    rules = (
        Rule(LinkExtractor(allow=r"http://category.dangdang.com/cp[\d|\.]*html"), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        item = JingdongItem()
        item['big_sort'] = response.xpath("//a[@dd_name='面包屑2级']/text()").get()
        item['small_sort'] = response.xpath("//a[@dd_name='面包屑3级']/text()").get()
        li_list = response.xpath("//ul[@class='bigimg']/li")
        for li in li_list:
            item['book_name'] = li.xpath("./a/@title").get()
            item['url'] = li.xpath("./a/@href").get()
            author = li.xpath(".//p[@class='search_book_author']/span[1]//text()").getall()
            if not author:
                author = li.xpath(".//p[@class='search_book_author']/text()").getall()
            item['author'] = ''.join(author)
            price = li.xpath(".//span[@class='search_now_price']/text()").get()
            item['price'] = re.sub('¥','', price)
            yield item
        next_url = response.xpath("//li[@class='next']/a/@href").get()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse_item)
