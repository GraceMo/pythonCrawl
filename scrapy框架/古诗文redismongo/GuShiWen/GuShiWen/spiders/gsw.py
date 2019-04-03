# -*- coding: utf-8 -*-
import scrapy
import re
import requests
from lxml import etree
from scrapy_redis.spiders import RedisSpider


class GswSpider(RedisSpider):
    name = 'gsw'
    allowed_domains = ['gushiwen.org']

    # start_urls = ['https://www.gushiwen.org/shiwen/default_3A{}A1.aspx'.format(i) for i in range(1,13)]
    # start_urls = ['https://www.gushiwen.org/shiwen/default_3A{}A1.aspx'.format(i) for i in range(1, 2)]
    # redis_key = 'gsw:s'
    def start_requests(self):
        url = ['https://www.gushiwen.org/shiwen/default_3A131313131313A1.aspx']
        start_urls = ['https://www.gushiwen.org/shiwen/default_3A{}A1.aspx'.format(i) for i in range(1, 13)]
        print('uuuu',start_urls)
        start_urls = start_urls+url
        print('kkkk',start_urls)
        for i in start_urls:
            yield scrapy.Request(url=i, callback=self.parse)

    def parse(self, response):
        sons = response.xpath("//div[@class='left']/div[@class='sons']")
        for son in sons:
            url = son.xpath(".//p[1]/a/@href").get()
            yield scrapy.Request(url, callback=self.detail)
        next = response.xpath("//a[text()='下一页']/@href").get()
        if next:
            next_url = response.urljoin(next)
            print('next_url', next_url)
            yield scrapy.Request(next_url, callback=self.parse)

    def detail(self, response):
        divFirst = response.xpath("//div[@class='left']/div")[0]
        name = divFirst.xpath(".//div[@class='cont']//h1/text()").get()
        dynasty = divFirst.xpath(".//p[@class='source']/a[1]/text()").get()
        author = divFirst.xpath(".//p[@class='source']/a[2]/text()").get()
        content = divFirst.xpath(".//div[@class='contson']//text()").getall()
        if len(content) > 0:
            content = ''.join(content).strip()
        item = {
            'name': name,
            'dynasty': dynasty,
            'author': author,
            'content': content,
            'url': response.url
        }
        sonspic = response.xpath("//div[@class='sonspic']")  # 作者简介
        if sonspic:
            div_list = response.xpath("//div[@class='left']/div")[1:-6]
        else:
            div_list = response.xpath("//div[@class='left']/div")[1:-5]
        for div in div_list:
            id = div.xpath("./@id").get()
            if id:
                if 'quan' in id:
                    continue
                eng = re.findall("\D+", id)[0]
                num = re.findall("\d+", id)[0]
                url = 'https://so.gushiwen.org/shiwen2017/ajax{}.aspx?id={}'.format(eng, num)
                h2, h3 = self.parse_ajax(url)
                item[h2] = h3
            else:
                contyishang = div.xpath("./div[@class='contyishang']//text()").getall()
                contyishang = ''.join(contyishang).strip()
                h2 = div.xpath("./div[@class='contyishang']//h2//text()").get()
                item[h2] = contyishang
        yield item

    def parse_ajax(self, url):
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'referer': 'https://so.gushiwen.org/shiwenv_4c5705b99143.aspx',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        }
        try:
            response = requests.get(url, headers=headers)
            text = response.content.decode()
            response = etree.HTML(text)
            h2 = response.xpath("//div[@class='contyishang']//h2/span/text()")
            h2 = h2[0] if len(h2) > 0 else 0
            h3 = response.xpath("//div[@class='contyishang']//p//text()")
            h3 = ''.join(h3).strip()
            h3 = re.sub('▲|\u3000|\n', '', h3)
            return h2, h3
        except:
            return '0', '0'
