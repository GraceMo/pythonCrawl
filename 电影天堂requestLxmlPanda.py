from lxml import etree
import requests
import pandas as pd
import re

'''
构造前5页url
解析每页response,得到每个movie的url,形成一个movie_url_list
请求每一个movie_url,解析网页得到数据
数据:movie_name
    ftp下载地址
    country产地
    year年代
    language语言
    count豆瓣评分
    length长度
    director导演
    actors主演
    '''


class DyttSpider():
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def get_pageurl_list(self):
        list1 = list(range(1, 6))  # [1,2,3,4,5]
        url_list = list(map(lambda x: self.url.format(x), range(1, 6)))  # url_list = pageurl_list
        pageurl_list = [self.url.format(i) for i in range(1, 5)]
        return pageurl_list

    def get_movie_info(self, url):
        movie_info_list = []
        print(url)
        movie_title = movie_name = english_name = country = language = count = director = actors = ftp = ''
        response = self.get_response(url).content.decode('gbk')
        html = etree.HTML(response)
        # movie_name = html.xpath("//font[@color='#07519a']//text()")[0]
        ftp = html.xpath("//td[@bgcolor='#fdfddf']/a/text()")[0]
        ptexts = html.xpath("//div[@id='Zoom']//p//text()")
        for index, content in enumerate(ptexts):
            movie_title = ptexts[0]
            if '译　　名' in content:
                english_name = re.sub('◎译　　名', '', content).strip()
            elif '片　　名' in content:
                movie_name = re.sub('◎片　　名', '', content).strip()
            elif '产　　地' in content:
                country = re.sub('◎产　　地', '', content).strip()
            elif '语　　言' in content:
                language = re.sub('◎语　　言', '', content).strip()
            elif '豆瓣评分' in content:
                count = re.sub('◎豆瓣评分', '', content).strip()
            elif '导　　演' in content:
                director = re.sub('◎导　　演', '', content).strip()
            elif '主　　演' in content:
                actor = re.sub('◎主　　演', '', content).strip()
                actors = [actor]
                for x in range(index + 1, len(ptexts)):  # 通过index开始循环
                    actor = ptexts[x].strip()
                    if actor.startswith('◎'):
                        break
                    actors.append(actor)
                actors = ','.join(actors)
        movie_info_list = [movie_title, movie_name, english_name, country, language, count, director, actors, ftp]
        return movie_info_list

    def get_response(self, url):
        response = requests.get(url, headers=self.headers, verify=False)
        return response  # content.decode('gb2312')

    def get_page_url(self, url):
        response = self.get_response(url).text
        html = etree.HTML(response)
        href = html.xpath("//div[@class='co_content8']/ul//a[@href]/@href")
        return ['http://www.ygdy8.net' + i for i in href]

    def save(self, movie_list):
        df = pd.DataFrame(data=movie_list,
                          columns=['标题', '电影名', '英文名', '国家', '语言', '评分', '导演', '主演', '下载地址'])
        df.to_csv('dytt.csv', index=False, encoding='utf-8-sig', mode='w')

    def run(self):
        page_url_list = self.get_pageurl_list()
        detail_url = []
        for url in page_url_list:
            page_movie_urls = self.get_page_url(url)
            detail_url += page_movie_urls
            print(len(detail_url))
        movie_list = []
        for url in detail_url:
            movie_info_list = self.get_movie_info(url)
            movie_list.append(movie_info_list)
        self.save(movie_list)


if __name__ == '__main__':
    url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_{}.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    }
    spider = DyttSpider(url, headers)
    spider.run()
