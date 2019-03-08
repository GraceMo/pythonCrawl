# -*- coding: utf-8 -*-
import scrapy
from urllib import request
from PIL import Image


class DbloginSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://accounts.douban.com/login?redir=https%3A%2F%2Fwww.douban.com%2F&source=index_nav']

    def parse(self, response):
        source = 'index_nav'
        redir = "https://www.douban.com/"
        form_email = "970138074@qq.com"
        form_password = "pythonspider"
        remember = 'on'
        login = '登录'
        formdata = {
            'source': source,
            'redir': redir,
            'form_email': form_email,
            'form_password': form_password,
            'remember': remember,
            'login': login,
        }
        captcha_image = response.xpath("//img[@id='captcha_image']/@src").extract_first()
        if captcha_image:
            formdata['captcha-id'] = response.xpath("//input[@name='captcha-id']/@value").extract_first()
            captcha = self.recognize_captcha(captcha_image)
            if not captcha:
                return scrapy.Request(url=self.start_urls[0], callback=self.parse)
            else:
                formdata['captcha-solution'] = captcha
        yield scrapy.FormRequest(url="https://accounts.douban.com/login", formdata=formdata, callback=self.parse_page)

    def parse_page(self, response):
        if response.url == 'https://www.douban.com/':
            print('登录成功！')
            # 进入个人中心，修改签名
            url = "https://www.douban.com/people/97956064/"
            yield scrapy.Request(url=url, callback=self.parse_person_info)
        else:
            print('登录失败！')
            yield scrapy.Request(url='https://accounts.douban.com/login', callback=self.parse, dont_filter=True)

    def parse_person_info(self, response):
        print('=' * 30)
        print(response.url)
        print('=' * 30)
        ck = response.xpath("//input[@name='ck']/@value").extract_first()
        signature = '我是scrapy修改的'
        yield scrapy.FormRequest(url="https://www.douban.com/j/people/97956064/edit_signature",
                                 formdata={"ck": ck, "signature": signature})

    def recognize_captcha(self, image_url):
        request.urlretrieve(image_url, 'captcha.png')
        image = Image.open('captcha.png')
        image.show()
        text = input('请输入验证码：')
        return text
