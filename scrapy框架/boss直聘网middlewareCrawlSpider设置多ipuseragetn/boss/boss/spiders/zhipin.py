# -*- coding: utf-8 -*-
import scrapy
from boss.items import BossItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ZhipinSpider(CrawlSpider):
    name = 'zhipin'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/c101010100-p100109/?page=1']
    rules = {
        Rule(LinkExtractor(allow='.*/c101010100-p100109/\?page=\d+'), follow=True),
        Rule(LinkExtractor(allow='.*/job_detail/.+\.html'), follow=False, callback='parse_detail')}

    def parse_detail(self, response):
        print(response.status)
        hr_name = response.xpath("//h2[@class='name']/text()").get().strip()
        title = response.xpath("//div[@class='info-primary']//h1/text()").get().strip()
        address = response.xpath(
            "//div[contains(@class,'detail-box')]//div[@class='info-primary']/p/text()").get().strip()
        salary = response.xpath("//span[@class='salary']/text()").get().strip()
        company_url = response.xpath("//div[@class='company-info']/a/@href").get().strip()
        company_url = "https://www.zhipin.com" + company_url
        company_name = response.xpath("//div[@class='company-info']/a/@title").get().strip()
        item = BossItem(title=title
                        , address=address
                        , hr_name=hr_name
                        , salary=salary
                        , company_name=company_name
                        , company_url=company_url)
        yield item
