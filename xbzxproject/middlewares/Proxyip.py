# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:v1.0
@var:随机代理
@note:默认每请求30条随机更换代理

"""

import random
import logging


# Start your middlewares class

class ProxyMiddleware(object):
    def __init__(self):
        self.idx = 0
        with open('E:\spider123\proxy.txt', 'rb')as f:
            proxy_list = f.readlines()
        self.proxy = random.choice(proxy_list)

    # overwrite process request
    def process_request(self, request, spider):
        self.idx += 1
        try:
            if spider.proxy:
                if self.idx >= 30:
                    self.idx = 0
                    with open('E:\spider123\proxy.txt', 'rb')as f:
                        proxy_list = f.readlines()
                    self.proxy = random.choice(proxy_list)
                    logging.warning("proxy is 50,random_proxy:{}".format(self.proxy))
                request.meta['proxy'] = "http://%s" % self.proxy
        except:
            logging.error(u"代理异常,请检查代理IP!")
