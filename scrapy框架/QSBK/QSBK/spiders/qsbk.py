# -*- coding: utf-8 -*-
import scrapy
from QSBK.items import QsbkItem


class QsbkSpider(scrapy.Spider):
    name = 'qsbk'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/']

    def parse(self, response):
        print(response.request.headers)
        divs = response.xpath("//div[@id='content-left']/div[@id]")
        for div in divs:
            name = div.xpath(".//h2/text()").extract_first().strip()
            content = div.xpath(
                ".//div[@class='content']/span//text()").extract()  # 获取字符串列表 == getall() extract_first == get()
            content = ''.join(content).strip()
            item = QsbkItem()
            item['name'] = name
            item['content'] = content
            # item = QsbkItem(name=name, content=content)
            yield item
        next_page_url = response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()
        print(next_page_url)
        if not next_page_url:
            return
        else:
            next_page_url = "https://www.qiushibaike.com" + next_page_url
            print(next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse)
