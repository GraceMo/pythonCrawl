import requests
import json

'''爬取豆瓣电视剧所有分类下的电影的名字/分数/链接'''


class Tv():
    def __init__(self, headers, item):
        self.headers = headers
        self.item = item
        self.movie_dict = {}

    def get_url_list(self, url):
        url_list = []
        for i in range(100):
            new_url = url.format(i * 20)
            url_list.append(new_url)
        return url_list

    def parse(self, url):
        response = requests.get(url, headers=self.headers)
        header = response.headers['Keep-Alive']
        print(header)  # timeout = 30
        return response.json()
        # return json.loads(response.content.decode())

    def get_data(self, response):
        for dict in response['subjects']:
            data = {}
            title = dict['title']
            rate = dict['rate']
            url = dict['url']
            cover_url = dict['cover']
            data['rate'] = rate
            data['url'] = url
            data['cover_url'] = cover_url
            self.movie_dict[title] = data

    def save(self):
        with open('./douban/%s.json' % self.item, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.movie_dict, ensure_ascii=False,indent=4))
        print(self.item, len(self.movie_dict))

    def run(self, url):
        '''
        构造爬取url列表
        获取响应,json格式
        提取title,url
        保存'''
        url_list = self.get_url_list(url)
        for url in url_list:
            response = self.parse(url)
            if len(response['subjects']) < 20:
                break
            print(url_list.index(url) + 1)
            self.get_data(response)
        self.save()


if __name__ == '__main__':
    items = ["热门", "美剧", "英剧", "韩剧", "日剧", "国产剧", "港剧", "日本动画", "综艺", "纪录片"]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Mobile Safari/537.36'}
    for item in items:
        url = 'https://movie.douban.com/j/search_subjects?type=tv&tag=%s&sort=recommend&page_limit=20&page_start={}' % item
        tvspider = Tv(headers, item)
        tvspider.run(url)
