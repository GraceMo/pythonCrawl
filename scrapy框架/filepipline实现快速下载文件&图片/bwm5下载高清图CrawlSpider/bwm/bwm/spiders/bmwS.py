# -*- coding: utf-8 -*-
import scrapy
from bwm.items import BwmItem
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

class BmwsSpider(CrawlSpider):   # todo 7
    name = 'bmwS'
    allowed_domains = ['car.autohome.com.cn','autoimg.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/65.html']
    rules = {
        Rule(LinkExtractor(allow=r'https://car.autohome.com.cn/pic/series/65-.*?\.html'),callback='parse_detail_urls',follow=True)
    }
    def parse_detail_urls(self, response):
        category = response.xpath("//div[@class='uibox']/div[@class='uibox-title']/text()").get()
        urls = response.xpath("//div[@class='uibox']//li//img/@src").getall()
        urls = list(map(lambda x:response.urljoin(x.replace('t_','')),urls))
        item = BwmItem(category=category,image_urls=urls)
        yield  item



    # def parse(self, response):
    #     uiboxs = response.xpath("//div[@class='uibox']")[1:]
    #     for uibox in uiboxs:
    #         cataegory = uibox.xpath(".//div[@class='uibox-title']/a[1]/text()").get()
    #         urls = uibox.xpath(".//ul/li/a/img/@src").getall()
    #         # for url in urls:
    #         #     url = response.urljoin(url)
    #         urls = list(map(lambda x: response.urljoin(x), urls))
    #         item = BwmItem(category=cataegory, image_urls=urls)  # todo 4
    #         yield item
