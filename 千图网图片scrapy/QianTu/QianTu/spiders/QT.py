# -*- coding: utf-8 -*-
import scrapy
from QianTu.items import QiantuItem


class QtSpider(scrapy.Spider):
    name = 'QT'
    allowed_domains = ['58pic.com', 'qiantucdn.com']
    start_urls = ['https://www.58pic.com/piccate/2-0-0-p1.html']
    i = 1

    def parse(self, response):
        #第一页所有详情页的url,对下一页发起请求
        pics = response.xpath("//div[@class='flow-box']/div")
        for pic in pics:
            title = pic.xpath(".//div[@class='card-img']//img/@alt").get()
            src = pic.xpath(".//div[@class='card-img']/a/@href").get()
            src = 'https:' + src
            item = QiantuItem(title=title)
            yield scrapy.Request(url=src, meta=item, callback=self.parse_detail)

        while self.i <= 284:
            self.i += 1
            print('第%s页' % self.i)
            url = 'https://www.58pic.com/piccate/2-0-0-p{}.html'.format(self.i)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_detail(self, response):
        #详情页中图片的url,发起请求,获取图片的字节流反馈
        item = response.meta
        img_list = response.xpath("//div[@id='show-area-height']/img/@src").getall()
        url = response.url
        url = url.replace('.html', '')
        meta = {'item': item,
                'refer': url}
        for url in img_list:
            url = 'https:' + url
            yield scrapy.Request(url, callback=self.parse_content, meta=meta)

    def parse_content(self, response):
        #保存图片的字节流到item中,交给pipelines保存<<在此保存比较好>>
        print('--cont---', response.body)
        item = response.meta.get('item')
        item['src'] = response.body
        yield item
