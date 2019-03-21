from scrapy import cmdline

cmdline.execute('scrapy crawl QT'.split())
#千图网爬取详情页图片,保存

#首页url发送请求,处理响应,提取详情页url,title
#详情页url,发送请求,处理响应,提取图片url,
#图片url,发送请求,接收响应,item接收,交给管道保存

#问题,图片url无法下载
#解决:请求图片url,设置请求头中Referer,设置为详情页url删除.html之后的url
