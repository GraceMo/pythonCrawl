# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
from jianshu.items import JianshuItem


class JianSpider(CrawlSpider):
    name = 'jian'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']
    rules = (
        Rule(LinkExtractor(allow='.*/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        title = response.xpath("//h1[@class='title']/text()").get()
        author = response.xpath("//div[@class='author']//span[@class='name']//text()").get()
        content = response.xpath("//div[@class='show-content-free']/p//text()").getall()
        content = ''.join(content)
        content = re.sub('\s|\xa0', '', content)
        url = response.url
        item = JianshuItem(
            title=title,
            author=author,
            content=content,
            url=url
        )
        yield item
