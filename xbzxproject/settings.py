# -*- coding: utf-8 -*-
# ! /usr/bin/env python

# Scrapy settings for xbzxproject project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import ConfigParser

PATH = "D:\\xbzx_webspider\\settings.ini"

conf = ConfigParser.ConfigParser()
conf.read(PATH)

# mysql
HOST = conf.get("mysql", "host")
PORT = int(conf.get("mysql", "port"))
USER = conf.get("mysql", "user")
PASSWD = conf.get("mysql", "passwd")
DATABASES = conf.get("mysql", "databases")

# proxy
PROXY_COUT = conf.get("proxy", "proxy_cout")
RANDOM_NUMBER = conf.get("proxy", "random_number")

# scrapy
PROJECT = conf.get("scrapy", "project")

# scrapyd
HOST_SCRAPYD = conf.get("scrapyd", "host")
PORT_SCRAPYD = conf.get("scrapyd", "port")


BOT_NAME = 'xbzxproject'

SPIDER_MODULES = ['xbzxproject.spiders']
NEWSPIDER_MODULE = 'xbzxproject.spiders'

LOG_LEVEL = "INFO"

COOKIE_DEBUG = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# scrapy-redis
# Enables scheduling storing requests queue in redis.
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# Ensure all spiders share same duplicates filter through redis.
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 3

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
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
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    #    'xbzxproject.middlewares.MyCustomSpiderMiddleware': 543,
    # 'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {

    'xbzxproject.middlewares.ProxyipMysql.ProxyMiddleware': 400,
    # 'scrapy_splash.SplashCookiesMiddleware': 723,
    # 'scrapyjs.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# DUPEFILTER_CLASS = 'scrapyjs.SplashAwareDupeFilter'
# SPLASH_URL = 'http://192.168.10.26:8050/'

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html

EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None,
    'xbzxproject.extensions.StatsPoster': 999,
}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'scrapy_redis.pipelines.RedisPipeline': 300,
    'xbzxproject.pipelines.XbzxprojectPipeline': 350,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# BASECONFIG 爬虫基本信息
# 贵州
# BASECONFIG = {
#     "mysql": {
#         "databases": "hlwsjcj",
#         "host": "172.16.20.96",
#         "port": 3306,
#         "user": "root",
#         "passwd": "westcredit123"
#     },
#     "scrapy": {
#         "project": "xbzxproject"
#     },
#     "scrapyd": {
#         "host": "172.16.20.96",
#         "port": 6800
#     }
# }

# BASECONFIG 爬虫基本信息
# 三亚
# BASECONFIG = {
#     "mysql": {
#         "databases": "DataCollectV3",
#         "host": "59.195.168.25",
#         "port": 3306,
#         "user": "root",
#         "passwd": "root"
#     },
#     "scrapy": {
#         "project": "xbzxproject"
#     },
#     "scrapyd": {
#         "host": "59.195.168.25",
#         "port": 6800
#     }
# }

# 青海
# BASECONFIG = {
#     "mysql": {
#         "databases": "DataCollectV1",
#         "host": "172.31.249.28",
#         "port": 3306,
#         "user": "root",
#         "passwd": "root"
#     },
#     "scrapy": {
#         "project": "xbzxproject"
#     },
#     "scrapyd": {
#         "host": "172.31.247.17",
#         "port": 6800
#     }
# }

# 山西
# BASECONFIG = {
#     "mysql": {
#         "databases": "DataCollectV1",
#         "host": "59.195.168.25",
#         "port": 3306,
#         "user": "root",
#         "passwd": "root"
#     },
#     "scrapy": {
#         "project": "xbzxproject"
#     },
#     "scrapyd": {
#         "host": "59.195.168.25",
#         "port": 6800
#     }
# }

# 西安
# BASECONFIG = {
#     "mysql": {
#         "databases": "zr_data_acq",
#         "host": "10.16.33.148",
#         "port": 3306,
#         "user": "zr_data_acq",
#         "passwd": "XbzxCaiji123"
#     },
#     "scrapy": {
#         "project": "xbzxproject"
#     },
#     "scrapyd": {
#         "host": "10.16.33.141",
#         "port": 6800
#     }
# }


# 公司
BASECONFIG = {
    "mysql": {
        "databases": "DataCollectV1",
        "host": "192.168.10.155",
        "port": 3306,
        "user": "root",
        "passwd": "root"
    },
    "scrapy": {
        "project": "xbzxproject"
    },
    "scrapyd": {
        "host": "192.168.10.173",
        "port": 6800
    }
}