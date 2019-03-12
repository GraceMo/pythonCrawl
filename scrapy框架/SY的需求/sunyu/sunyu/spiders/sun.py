# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from sunyu.items import SunyuItem
import re
class SunSpider(CrawlSpider):
    name = 'sun'
    allowed_domains = ['dzzsw.cn']
    start_urls = ['http://www.dzzsw.cn/vodtypehtml/16.html']

    rules = (
        Rule(LinkExtractor(allow=r'.*/vodtypehtml/16(-\d{1,3}|)\.html'), follow=True,callback='parse_detail'),# 1
        # Rule(LinkExtractor(allow=r'.*/vodtypehtml/16(|)\.html'), follow=False,callback='parse_detail'),
    )

    def parse_detail(self, response):
        lis = response.xpath(".//ul[@class='mlist']/li")
        for li in lis:
            name = li.xpath("./a/@title").get()
            url2 = li.xpath("./a/@href").get()
            num = re.search("(\d+)",url2).group(1)
            url3 = 'http://www.dzzsw.cn/vodplayhtml/%s.html?/%s-1-1'%(num,num)
            print(url3)
            yield scrapy.Request(url3,callback=self.parse_item,meta={'name':name})

    def parse_item(self,response):
        name = response.meta.get('name')
        item = SunyuItem()
        item['name'] = name
        item['url'] = response.xpath("//iframe[@class='embed-responsive-item']/@src").get()
        print('spider======----------========')
        yield item


