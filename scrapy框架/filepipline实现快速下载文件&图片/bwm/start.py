from scrapy import cmdline

cmdline.execute('scrapy crawl bmwS'.split())

# todo 1-4步,改用scrapyimagesPipline,实现异步下载
# todo 5-6   重写imagesPipline中的file_path方法,实现图片分类
