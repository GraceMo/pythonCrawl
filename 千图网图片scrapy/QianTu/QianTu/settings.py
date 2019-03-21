# -*- coding: utf-8 -*-

# Scrapy settings for QianTu project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'QianTu'

SPIDER_MODULES = ['QianTu.spiders']
NEWSPIDER_MODULE = 'QianTu.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'QianTu (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
# DEG_LOG = 'WARNING'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.9
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    # 'Host': 'www.58pic.com',
    'Referer': 'https://www.58pic.com/',
    'Upgrade-Insecure-Requests': '1',
    'Cookie': 'message2=1; qt_visitor_id=%227c2de6547f4c49f29246574e2909d611%22; user-browser=%22baidu%22; message2=1; FIRSTVISITED=1553091397.324; qt_ur_type=2; awake=0; qt_type=2; imgCodeKey=%224de7420dbf409067c9775369964ab74d%22; risk_forbid_login_uid=%2253662979%22; auth_id=%2253662979%7CH+e+ll+o%7C1553696271%7C9f9b49f173bf0883f2af79e9b1a2f8b9%22; success_target_path=%22https%3A%5C%2F%5C%2Fwww.58pic.com%5C%2Fnewpic%5C%2F28478935.html%22; sns=%7B%22token%22%3A%7B%22access_token%22%3A%227D7133797BC4AD161CFB27643CB49127%22%2C%22expires_in%22%3A%227776000%22%2C%22refresh_token%22%3A%2283D7D3140DDE1E480D3AD869A125A7B7%22%2C%22openid%22%3A%22D4C295E47376BF58257C18CCC3A38592%22%7D%2C%22type%22%3A%22qq%22%7D; ssid=%225c924b8f5e4b94.84725367%22; _is_pay=0; sns_uid=53662979; qt_uid=%2253662979%22; _uab_collina=155309147304271511641072; ISREQUEST=1; WEBPARAMS=is_pay=0; censor=%2220190321%22; Hm_lvt_41d92aaaf21b7b22785ea85eb88e7cea=1553091396,1553092943,1553144115; qiantudata2018jssdkcross=%7B%22distinct_id%22%3A%221699b760127893-038ad5db33f6c3-3a614f0b-1327104-1699b760128c6d%22%2C%22props%22%3A%7B%22latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22latest_referrer_host%22%3A%22www.baidu.com%22%2C%22latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; Hm_lvt_2c2888b2fe22cba4fac6b948cd7e7834=1553091396,1553091473,1553092943,1553144117; Hm_lvt_644763986e48f2374d9118a9ae189e14=1553091400,1553092943,1553144118; han_data_is_pay:53662979=%222%22; source_lookp=%2228467816-https%3A%5C%2F%5C%2Fwww.58pic.com%5C%2Fc%5C%2F14326784%22; Hm_lpvt_41d92aaaf21b7b22785ea85eb88e7cea=1553145097; Hm_lpvt_2c2888b2fe22cba4fac6b948cd7e7834=1553145098; Hm_lpvt_644763986e48f2374d9118a9ae189e14=1553145099; qt_utime=1553145100'}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'QianTu.middlewares.QiantuSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'QianTu.middlewares.QiantuDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'QianTu.pipelines.QiantuPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
