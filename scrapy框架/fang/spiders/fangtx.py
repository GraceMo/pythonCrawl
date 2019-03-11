# -*- coding: utf-8 -*-
import scrapy
import re
from fang.items import NewHouse,EsfHouse
from scrapy_redis.spiders import RedisSpider # 1

class FangtxSpider(scrapy.Spider):
    name = 'fangtx'
    allowed_domains = ['fang.com']
    start_urls = ['http://www.fang.com/SoufunFamily.htm']  # 2
    # redis_key = 'fang:start_urls'

    def parse(self, response):
        trs = response.xpath("//div[@class='outCont' and @id='c02']//tr")
        province = None
        for tr in trs:
            province_text = tr.xpath("./td[2]//text()").extract_first()
            province_text = re.sub(r'\s', '', province_text)
            if province_text:
                province = province_text
            if province == '其它':
                continue
            city_as = tr.xpath("./td[3]/a")
            for a in city_as:
                city_name = a.xpath("./text()").extract_first()
                city_href = a.xpath("./@href").extract_first()
                new_house_url, esf_url = self.new_erf_url(city_href)
                info = [province, city_name, new_house_url]
                info2 = [province, city_name, esf_url]
                # yield scrapy.Request(url=new_house_url, callback=self.parse_newhouse, meta={'info': info})
                yield scrapy.Request(url=esf_url, callback=self.parse_esf, meta={'info': info2})
                # yield scrapy.Request(url=esf_url, callback=self.parse_esf, meta={'info': info2})

                break
            break


    def parse_newhouse(self, response):
        province, city_name, new_house_url = response.meta.get('info')
        lis = response.xpath("//div[contains(@class,'nl_con')]/ul/li")
        for li in lis:
            h3 = li.xpath(".//h3/text()").extract_first()
            if h3:
                continue
            name = li.xpath(".//div[@class='nlcd_name']/a/text()").get().strip()
            house_type_list = li.xpath(".//div[contains(@class,'house_type')]/a/text()").getall()
            house_type_list = list(map(lambda x: re.sub(r"\s", '', x), house_type_list))
            rooms = list(filter(lambda x: x.endswith('居'), house_type_list))
            area = ''.join(li.xpath(".//div[contains(@class,'house_type')]/text()").getall())
            area = re.sub(r"\s|/|－", '', area)
            address = li.xpath(".//div[@class='address']/a/@title").get()
            district_text = ''.join(li.xpath(".//div[@class='address']/a//text()").getall())
            try:
                district = re.search(r".*\[(.+)\].*", district_text).group(1)
            except:pass
            sale = li.xpath(".//div[contains(@class,'fangyuan')]/span/text()").get()
            price = ''.join(li.xpath(".//div[@class='nhouse_price']//text()").getall())
            price = re.sub(r"\s|广告", '', price)
            origin_url = li.xpath(".//div[@class='nlcd_name']/a/@href").get()
            item = NewHouse(name=name, rooms=rooms, area=area, address=address, district=district, sale=sale,
                            price=price, origin_url=origin_url, province=province, city_name=city_name)
            print('newHOuse',dict(item))
            yield item
        # url_list = new_house_url.split('/')
        # next_url = response.xpath(".//a[text()='下一页']/@href").extract_first()
        # if next_url:
        #     next_url = 'http://' + url_list[2] + next_url
        #     print("nexturl", next_url)
        #     yield scrapy.Request(url=next_url, callback=self.parse_newhouse, meta=response.meta)

    def parse_esf(self, response):
        province, city_name, new_house_url = response.meta.get('info')
        dls = response.xpath("//div[@class='houseList']/dl")
        for dl in dls:
            item = EsfHouse(province=province,city_name=city_name)
            item['name'] = dl.xpath(".//p[@class='mt10']/a/span/text()").get()
            infos = dl.xpath(".//p[@class='mt12']/text()").getall()
            infos = list(map(lambda x:re.sub(r"\s","",x),infos))
            for info in infos:
                if "厅" in info:
                    item['rooms'] = info
                elif '层' in info:
                    item['floor'] = info
                elif '向' in info :
                    item['toward'] = info
                else:
                    item['year'] = info.replace('建筑年代:','')
            item['address'] = dl.xpath(".//p[@class='mt10']/span/@title").get()
            item['area'] = dl.xpath(".//div[contains(@class,'area')]/p/text()").get()
            item['price'] = ''.join(dl.xpath(".//div[@class='moreInfo']/p[1]//text()").getall())
            item['unit'] = ''.join(dl.xpath(".//div[@class='moreInfo']/p[2]//text()").getall())
            detail_url = dl.xpath(".//p[@class='title']/a/@href").get()
            item['origin_url'] = response.urljoin(detail_url)
            print('erf', dict(item))

            yield item
        # next_url = response.xpath(".//a[text()='下一页']/@href").extract_first()
        # if next_url:
        #     yield scrapy.Request(url=response.urljoin(next_url),callback=self.parse_esf,meta=response.meta)

    def new_erf_url(self, city_href):
        if 'bj' in city_href:
            new_house = 'http://newhouse.fang.com/house/s/'
            esf_house = 'http://esf.fang.com/'
        else:
            url_list = city_href.split('.', 1)
            new_house = url_list[0] + '.newhouse.' + url_list[1] + 'house/s/'
            esf_house = url_list[0] + '.esf.' + url_list[1]
        print(new_house,esf_house)
        return new_house, esf_house
