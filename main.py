# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:
@var:
@note:

"""
import json
import os
import uuid
from scrapy import cmdline


def main():
    # with open(u'webconfig.json', u'rb')as f:
    #     txt = f.read()
    #
    # webconf = json.loads(txt)
    # scrapy = webconf.get(u"scrapy")
    # path = scrapy.get(u"path")
    uid = uuid.uuid1().hex
    scrapyrun = "scrapy crawl news -a name_spider=runspider -a spider_jobid=%s" % uid
    cmdline.execute(scrapyrun.split())


if __name__ == "__main__":
    main()
