# -*- coding: utf-8 -*-
import scrapy
import re
from SouFang.items import NewHouseItem, EsfItem
from scrapy_redis.spiders import RedisSpider

class FangSpider(RedisSpider):   # todo 1
    name = 'fang'
    allowed_domains = ['fang.com']
    # start_urls = ['https://www.fang.com/SoufunFamily.htm']  # todo 2
    redis_key = 'fang:start_url'

    def parse(self, response):
        trs = response.xpath("//div[@id='c02']//table[@class='table01']//tr")
        province = None
        for tr in trs:
            province_text = tr.xpath(".//td[2]//text()").get().strip()
            if province_text:
                province = province_text
            if province == '其它':
                continue
            a_list = tr.xpath(".//a")
            for a in a_list:
                city_href = a.xpath("./@href").get().strip()
                city_name = a.xpath("./text()").get().strip()
                before, after = city_href.split('.', 1)
                if after.endswith('/'):
                    newHouse_href = before + '.newhouse.' + after + 'house/s/'
                else:
                    newHouse_href = before + '.newhouse.' + after + '/house/s/'
                esf_href = before + '.esf.' + after
                if city_name == '北京':
                    esf_href = 'https://esf.fang.com/'
                    newHouse_href = 'https://newhouse.fang.com/house/s/'
                yield scrapy.Request(newHouse_href, callback=self.parse_newHouse, meta={'info': (province, city_name)})
                # yield scrapy.Request(esf_href, callback=self.parse_esf, meta={'info': (province, city_name)})

    def parse_newHouse(self, response):
        province, city_name = response.meta.get('info')
        li_list = response.xpath("//div[@class='nhouse_list']//li")
        for li in li_list:
            pictr = li.xpath(".//div[@class='pictr']").get()
            if pictr:
                continue
            house_name = li.xpath(".//div[@class='nlcd_name']//text()").get()
            house_name = house_name.strip()

            address = li.xpath(".//div[@class='address']/a/@title").get()
            district = li.xpath(".//div[@class='address']//text()").getall()
            district = ''.join(district)
            district = re.search('\[(.*?)\]',district).group(1)

            house_type = li.xpath(".//div[contains(@class,'house_type')]//a/text()").getall()
            area = li.xpath(".//div[contains(@class,'house_type')]/text()").getall()
            area = ''.join(area)
            area = re.sub('\s|/|－', '', area)
            price = li.xpath(".//div[@class='nhouse_price']//text()").getall()
            price = ''.join(price).strip()
            house_url = li.xpath(".//div[@class='nlcd_name']/a/@href").get()
            house_url = response.urljoin(house_url)
            onsale = li.xpath(".//div[contains(@class,'fangyuan')]/span/text()").get()
            label = li.xpath(".//div[contains(@class,'fangyuan')]/a/text()").getall()
            labels = ','.join(label)
            item = NewHouseItem(
                house_name=house_name,
                address=address,
                district=district,
                house_type=house_type,
                area=area,
                price=price,
                house_url=house_url,
                labels=labels,
                onsale=onsale,
            )
            print(dict(item))
            yield item
        next_url = response.xpath("//a[text()='下一页']/@href").get()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse_newHouse, meta=response.meta)



    def parse_esf(self, response):
        province, city_name, new_house_url = response.meta.get('info')
        dls = response.xpath("//div[@class='houseList']/dl")
        for dl in dls:
            item = EsfItem(province=province, city_name=city_name)
            item['name'] = dl.xpath(".//p[@class='mt10']/a/span/text()").get()
            infos = dl.xpath(".//p[@class='mt12']/text()").getall()
            infos = list(map(lambda x: re.sub(r"\s", "", x), infos))
            for info in infos:
                if "厅" in info:
                    item['rooms'] = info
                elif '层' in info:
                    item['floor'] = info
                elif '向' in info:
                    item['toward'] = info
                else:
                    item['year'] = info.replace('建筑年代:', '')
            item['address'] = dl.xpath(".//p[@class='mt10']/span/@title").get()
            item['area'] = dl.xpath(".//div[contains(@class,'area')]/p/text()").get()
            item['price'] = ''.join(dl.xpath(".//div[@class='moreInfo']/p[1]//text()").getall())
            item['unit'] = ''.join(dl.xpath(".//div[@class='moreInfo']/p[2]//text()").getall())
            detail_url = dl.xpath(".//p[@class='title']/a/@href").get()
            item['origin_url'] = response.urljoin(detail_url)
            yield item
        next_url = response.xpath(".//a[text()='下一页']/@href").extract_first()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse_esf, meta=response.meta)

