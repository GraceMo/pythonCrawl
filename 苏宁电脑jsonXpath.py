import requests, re, json
from lxml import etree

'''
所有电脑的title  price  config  href
{1:{title:'',price:'',},2:...}
{3:{title:'',price:'',},4:...}
1.获取url列表
2.单个url爬取
3.分析网页,re,获取数据
4.保存数据
'''
'https://list.suning.com/emall/searchV1Product.do?ci=258004&pg=03&cp=1&il=0&st=8&iy=0&adNumber=5&n=1&sesab=ACBAAB&id=IDENTIFYING&cc=010&sub=0'
'https://list.suning.com/emall/searchV1Product.do?ci=258004&pg=03&cp=1&il=0&st=8&iy=0&adNumber=5&n=1&sesab=ACBAAB&id=IDENTIFYING&cc=010&paging=2&sub=0&jzq=24719'

class SNSpider():
    def __init__(self, headers):
        self.i = 1
        self.headers = headers

    def get_url_list(self, url):
        url_list = []
        for i in range(1, 6):
            new_url = url.format(i, '')
            url_list.append(new_url)
            for j in range(1, 4):
                new_url_u = url.format(i, '&paging=%d&' % j)
                url_list.append(new_url_u)
        print(len(url_list))
        return url_list

    def get_response(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def get_data(self, text):
        dict_1 = {}
        html = etree.HTML(text)
        li_list = html.xpath('//li[@doctype]')
        for sa in li_list:
            dict_2 = {}
            title = sa.xpath('.//div[@class="title-selling-point"]/a/text()')[0] if len(
                sa.xpath('//div[@class="title-selling-point"]/a/text()')) > 0 else None
            href = sa.xpath('.//div[@class="title-selling-point"]/a/@href')[0] if len(
                sa.xpath('//div[@class="title-selling-point"]/a/@href')) > 0 else None
            dict_2['name'] = title
            dict_2['href'] = href
            dict_1[self.i] = dict_2
            self.i += 1
        return dict_1

    def save(self, data):
        with open('sn.json', 'a', encoding='utf8')as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=4))

    def run(self, url):
        url_list = self.get_url_list(url)
        for url in url_list:
            print(url)
            text = self.get_response(url)
            data = self.get_data(text)
            self.save(data)


if __name__ == "__main__":
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    url = 'https://list.suning.com/emall/searchV1Product.do?ci=258004&pg=03&cp={}&il=0&st=8&iy=0&adNumber=5&n=1&sesab=ACBAAB&id=IDENTIFYING&cc=010{}&sub=0'
    spider = SNSpider(headers)
    spider.run(url)
