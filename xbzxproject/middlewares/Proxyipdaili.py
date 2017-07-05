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

import logging


class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        try:
            request.meta['proxy'] = "http://172.16.20.92:808"
        except:
            logging.error(u"代理异常,请检查代理IP!")
