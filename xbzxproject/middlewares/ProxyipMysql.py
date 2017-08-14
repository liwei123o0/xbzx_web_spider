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
import MySQLdb
from xbzxproject.utils.loadconfig import loadscrapyconf


# Start your middlewares class

class ProxyMiddleware(object):
    def __init__(self):
        self.idx = 0
        self.conf = loadscrapyconf()['mysql']
        self.conn = MySQLdb.connect(host=self.conf.get("host", "localhost"),
                                    port=self.conf.get("port", 3306),
                                    user=self.conf.get("user", "root"),
                                    passwd=self.conf.get("passwd", "root"),
                                    db=self.conf.get("databases"), charset=u"utf8")
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT proxyip FROM net_proxy;")
        self.proxies = self.cur.fetchall()
        if len(self.proxies) == 0:
            self.proxies = ((["127.0.0.1:8080"], ["127.0.0.1:8088"]))
        self.proxy = random.choice(self.proxies)[0]
        self.cur.close()
        self.conn.close()

    # overwrite process request
    def process_request(self, request, spider):
        self.idx += 1
        try:
            if spider.proxy:
                if self.idx >= 50:
                    self.idx = 0
                    self.proxy = random.choice(self.proxies)[0]
                    logging.warning("proxy is 50,random_proxy:{}".format(self.proxy))
                request.meta['proxy'] = "http://%s" % self.proxy
        except:
            logging.error(u"代理异常,请检查代理IP!")


if __name__ == "__main__":
    pass
