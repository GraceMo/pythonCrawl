# -*- coding: utf8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wxapp.items import WxappItem


class WxappWxSpider(CrawlSpider):
    name = 'wxapp_wx'
    allowed_domains = ['wxapp-union.com']
    start_urls = ['http://www.wxapp-union.com/portal.php?mod=list&catid=2']
    rules = (
        Rule(LinkExtractor(allow=r'.+mod=list&catid=2&page=\d{1,3}'), follow=True),
        Rule(LinkExtractor(allow=r'article[-\d]*?\.html'), callback='parse_detail', follow=False),
    )

    def parse_detail(self, response):
        div_bm = response.xpath("//div[@class='bm vw']")[0]
        title = div_bm.xpath("//h1[@class='ph']/text()").get()
        author = div_bm.xpath("//p[@class='authors']/a/text()").get()
        time = div_bm.xpath("//p[@class='authors']/span/text()").get()
        info = div_bm.xpath("//div[@class='blockquote']/p/text()").get()
        url = response.url
        item = WxappItem(title=title, author=author, time=time, info=info, url=url)
        print(dict(item))
        print("****")
        yield item
