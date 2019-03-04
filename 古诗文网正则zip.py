import re, requests, json

'''
构造url列表
解析网页,re
json格式{poem_name:{author:xx,dynasty:xx,content:xx,url:xx}
'''


class GuShiSpider():
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.poem_dict = {}

    def parse_data(self, text):
        poem_names = re.findall('<div class="sons">.*?target="_blank"><b>(.*?)</b>', text, re.DOTALL)
        authors = re.findall('<p class="source"><a href=.*?</span><a href=.*?>(.*?)</a>', text, re.S)
        dynastys = re.findall('<p class="source"><a href=.*?>(.*?)</a>', text, re.S)
        contents = re.findall('<div class="contson".*?">(.*?)</div>', text, re.S)
        contents = [re.sub('[a-zA-Z/\s<>\n="-:]*|<p><span style="font-family:SimSun;">', '', content) for content in
                    contents]
        urls = re.findall(
            '<p><a style="font-size:18px; line-height:22px; height:22px;" href="(.*?)" target="_blank"><b>', text)
        for poem in zip(poem_names, authors, dynastys, contents, urls):
            in_dict = {}
            poem_name = poem[0]
            in_dict['author'] = poem[1]
            in_dict['dynasty'] = poem[2]
            in_dict['content'] = poem[3]
            in_dict['url'] = poem[4]
            self.poem_dict[poem_name] = in_dict

    def save(self):
        print(len(self.poem_dict))
        print('古诗名目:', self.poem_dict.keys())
        with open('古诗.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.poem_dict, ensure_ascii=False, indent=4))

    def run(self):
        url_list = [self.url.format(i) for i in range(1, 11)]
        for url in url_list:
            text = requests.get(url, headers=self.headers).text
            self.parse_data(text)
        self.save()


if __name__ == '__main__':
    url = 'https://www.gushiwen.org/shiwen/default_0AA{}.aspx'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    spider = GuShiSpider(url, headers)
    spider.run()

# with open('古诗.json','r',encoding='utf8')as f:
#     content = json.loads(f.read())
