# -*- coding: utf-8 -*-
import scrapy,re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jingdong.items import JingdongItem
from scrapy_redis.spiders import RedisCrawlSpider

class AmazonSpider(RedisCrawlSpider):
    name = 'amazon'
    allowed_domains = ['amazon.cn']
    # start_urls = ['https://www.amazon.cn/gp/book/all_category']
    redis_key = 'amazon:s'
    rules = (
        #首页分类
        Rule(LinkExtractor(restrict_xpaths=("//table[@class='a-normal a-align-center a-color-base seo-booksitemap-content-table']")), callback='parse_item',follow=False),
        #翻页
        Rule(LinkExtractor(restrict_xpaths=("//div[@id='pagn']")),callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = JingdongItem()
        item['big_sort'] = response.xpath("//span[@id='s-result-count']/span/a[2]/text()").get()
        item['small_sort'] = response.xpath("//span[@id='s-result-count']/span/span/text()").get()
        li_list = response.xpath("//div[@id='mainResults']//li")
        for li in li_list:
            item['book_name'] = li.xpath(".//div/div[2]/div[1]/div[1]/a/h2/text()").get()
            author = li.xpath(".//div[@class='a-row a-spacing-small']/div[last()]/span/text()").getall()
            item['author'] = ','.join(author)
            item['url'] = li.xpath(".//a[@class='a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal']/@href").get()
            item['price'] = li.xpath(".//div[@class='a-column a-span7']//a[@title='精装' or @title='平装']/../following-sibling::div[1]/a//text()").get()
            # item['price'] = re.sub('￥','',price)
            yield item


