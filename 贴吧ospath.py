import requests
import os


class TieBaSpider():
    def __init__(self, tie_name):
        self.tie_name = tie_name
        self.url = 'https://tieba.baidu.com/f?kw=' + tie_name + '&pn={0}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

    def get_url_list(self):
        return [self.url.format(i * 50) for i in range(3)]

    def parse_html(self, url):
        response = requests.get(url, headers=self.headers)
        return response.text

    def save_html(self, html_str, page_num):
        file_name = '{}吧-第{}页.html'.format(self.tie_name, page_num)
        # file_name = './tieba/{}'.format(file_name)
        file_name = os.path.join(os.getcwd(), 'tieba', file_name)
        with open(file_name, 'w', encoding='utf8')as f:
            f.write(html_str)
        print('success')

    def run(self):
        '''
        构造url列表
        爬取网页
        保存网页
        '''
        url_list = self.get_url_list()
        for url in url_list:
            html_str = self.parse_html(url)
            page_num = url_list.index(url) + 1
            self.save_html(html_str, page_num)


if __name__ == '__main__':
    tieb_name = input('输入贴吧名字>>')
    spider = TieBaSpider(tieb_name)
    spider.run()
