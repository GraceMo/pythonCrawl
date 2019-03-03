import requests
from bs4 import BeautifulSoup

'''
通过login_url获取authenticity_token信息,补全post_data,
发送post_url登陆,获取cookies
携带cookies登陆logined_url,保存页面
'''


class LoginGithub():
    def __init__(self, email, password, headers):
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.logined_url = 'https://github.com/GraceMo?tab=repositories'
        self.headers = headers
        self.email = email
        self.password = password
        self.session = requests.Session()

    def get_authen(self):
        response = self.session.get(self.login_url, headers=self.headers)
        response.encoding = response.apparent_encoding
        html = BeautifulSoup(response.text, 'lxml')
        value = html.find('input', attrs={'name': 'authenticity_token'})['value']
        return value

    def run(self):
        post_data = {
            'commit	': 'Sign+in',
            'utf8': '✓',
            'authenticity_token': self.get_authen(),
            'login': self.email,
            'password': self.password
        }
        self.session.post(self.post_url, data=post_data, headers=self.headers)
        response2 = self.session.get('https://www.baidu.com', headers=self.headers)
        with open('github.html', 'w', encoding='utf8') as f:
            f.write(response2.content.decode())


if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
        'Host': 'github.com',
        'Referer': 'https://github.com'
    }
    email = 'email'
    password = 'password'
    login = LoginGithub(email, password, headers)
    login.run()
