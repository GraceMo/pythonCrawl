'''多线程下载斗图吧表情包
单线程下载
    构造url列表
    爬取每页img_url列表
    下载
改为多线程
    threading
    Queue
'''
import requests
from lxml import etree
import re
import os
from urllib import request
import threading
from queue import Queue


class Producer(threading.Thread):
    def __init__(self, page_queue, img_queue, *args, **kwargs):
        super(Producer, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        }

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            print('page_queue_size:', self.page_queue.qsize())
            response = requests.get(url, headers=self.headers)
            html = etree.HTML(response.text)
            img_tags = html.xpath("//div[@class='col-sm-9']//img[@class!='gif']")
            for img_tag in img_tags:
                img_url = img_tag.xpath("./@data-backup")[0]
                img_url = re.sub('!dta', '', img_url)
                title = img_tag.xpath("./@alt")[0]
                suffix = os.path.splitext(img_url)[1]
                file_name = title + suffix
                file_name = re.sub('[/\*\?: !\|<>"]*', '', file_name)
                self.img_queue.put((img_url, file_name))


class Consumer(threading.Thread):
    def __init__(self, page_queue, img_queue, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.page_queue.empty() and self.img_queue.empty():
                break
            img_url, file_name = self.img_queue.get()
            print(file_name)
            print('img_queue_size', self.img_queue.qsize())
            request.urlretrieve(img_url, 'meme/' + file_name)


if __name__ == '__main__':
    page_queue = Queue(100)
    img_queue = Queue(2000)
    for i in range(1, 101):
        url = 'http://www.doutula.com/article/list/?page=%d' % i
        page_queue.put(url)
    for i in range(10):
        p = Producer(page_queue, img_queue)
        p.start()
    for i in range(10):
        c = Consumer(page_queue, img_queue)
        c.start()
