# -*- coding: utf-8 -*-
import scrapy
from jingdong.items import JingdongItem
import json
from copy import deepcopy
from scrapy_redis.spiders import RedisSpider

class JdSpider(RedisSpider):
    name = 'jd'
    allowed_domains = ['jd.com', 'p.3.cn']
    # start_urls = ['https://book.jd.com/booksort.html']
    redis_key = 'jd:start_url'

    def parse(self, response):
        dts = response.xpath("//div[@class='mc']/dl/dt")
        dds = response.xpath("//div[@class='mc']/dl/dd")
        for dt in dts:
            big_sort = dt.xpath("./a/text()").get()
            inde = dts.index(dt)
            dd = dds[inde]
            ems = dd.xpath("./em")
            for em in ems:
                small_sort = em.xpath("./a/text()").get()
                href = em.xpath("./a/@href").get()
                href = 'https:' + href
                item = JingdongItem(big_sort=big_sort,
                                    small_sort=small_sort)
                yield scrapy.Request(href, callback=self.parse_detail, meta={'item': deepcopy(item)})
        # 下一页
        next_url = response.xpath("//a[@class='pn-next']/@href").get()
        if next_url:
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta.get('item')
        lis = response.xpath("//div[@id='plist']//li")
        for li in lis:
            book_name = li.xpath(".//div[@class='p-name']/a/em/text()").get().strip()
            author = li.xpath(".//span[@class='author_type_1']/a/text()").getall()
            author = ','.join(author)
            url = li.xpath(".//div[@class='p-img']/a/@href").get()
            url = 'https:' + url
            item['url'] = url
            item['book_name'] = book_name
            item['author'] = author
            num = li.xpath("./div/@data-sku").get()
            price_url = 'https://p.3.cn/prices/mgets?skuIds=J_{}'.format(num)
            yield scrapy.Request(price_url, callback=self.price, meta={'item': deepcopy(item)})

    def price(self, response):
        item = response.meta.get('item')
        data = json.loads(response.body.decode())
        price = data[0]['op']
        item['price'] = price
        yield item
