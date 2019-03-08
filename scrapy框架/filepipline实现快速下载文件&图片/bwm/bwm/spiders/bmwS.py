# -*- coding: utf-8 -*-
import scrapy
from bwm.items import BwmItem


class BmwsSpider(scrapy.Spider):
    name = 'bmwS'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/65.html#pvareaid=3454438']

    def parse(self, response):
        uiboxs = response.xpath("//div[@class='uibox']")[1:]
        for uibox in uiboxs:
            cataegory = uibox.xpath(".//div[@class='uibox-title']/a[1]/text()").get()
            urls = uibox.xpath(".//ul/li/a/img/@src").getall()
            # for url in urls:
            #     url = response.urljoin(url)
            urls = list(map(lambda x: response.urljoin(x), urls))
            item = BwmItem(category=cataegory, image_urls=urls)  # todo 4
            yield item
