from urllib import request, parse
from http.cookiejar import CookieJar

'''
登陆人人,获取cookies
访问其他个人网页
'''


class RenRenSpider():
    def __init__(self, login_url, person_url, headers, data):
        self.login_url = login_url
        self.person_url = person_url
        self.data = parse.urlencode(data).encode('utf-8')
        self.headers = headers

    def get_req(self, url, data=None):
        req = request.Request(url,data=data,headers=self.headers)
        return req

    def get_cookies(self):
        cookiejar = CookieJar()  # 1 创建一个cookiejar对象
        handler = request.HTTPCookieProcessor(cookiejar)  # 2 使用cookiejar创建一个HTTPCookieProcess对象
        opener = request.build_opener(handler)  # 3 使用上一步创建的handler创建一个opener
        req = self.get_req(self.login_url, data=self.data)  # 4 构建Request对象
        opener.open(req)  # 5 请求登陆,成功之后自动携带cookies
        return opener

    def visit_personal_page(self, opener):
        req = self.get_req(self.person_url)
        response = opener.open(req)
        with open('renren.html', 'w', encoding='utf-8') as f:
            f.write(response.read().decode())

    def run(self):
        opener = self.get_cookies()
        self.visit_personal_page(opener)

if __name__ == '__main__':
    login_url = 'http://www.renren.com/PLogin.do'
    person_url = 'http://www.renren.com/969896126/profile'
    data = {'email': '123',
            'password': '123'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    spider = RenRenSpider(login_url, person_url, headers, data)
    spider.run()
