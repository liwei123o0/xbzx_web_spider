# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:V1.0
@var:新闻类通用模版
@note:新闻通用模版采集~必须字段: spider_jobid name_spider

"""
from scrapy import Item, Field
from scrapy.spiders import CrawlSpider
from xbzxproject.utils.loadconfig import loadMySQL, fileconfig, loadkeywords
import logging
import json
from scrapy.selector import Selector
from scrapy.http import Request


class SearchSpider(CrawlSpider):
    name = "search_list"

    # 加载规则配置文件
    # 获取额外参数
    def __init__(self, spider_jobid=None, name_spider=None, debug=False, *args, **kwargs):
        self.spider_jobid = spider_jobid
        self.name_spider = name_spider
        self.debug = debug
        self.loadconf(name_spider, spider_jobid)
        self.conf = fileconfig(name_spider)
        super(SearchSpider, self).__init__(*args, **kwargs)

    # 传递搜索关键词及搜索连接
    def start_requests(self):
        if self.conf.get("keywords", "") == "":
            keywords = loadkeywords()
        else:
            keywords = self.conf.get("keywords").split(",")
        for word in keywords:
            if type(word) == tuple:
                word = " ".join(word)
            url = self.conf.get("start_urls", "").format(word=word)
            yield Request(url, callback=self.loadconf(self.name_spider, self.spider_jobid), meta={'word': word})

    # 规则配置
    def loadconf(self, name_spider, spider_jobid):

        if name_spider == None or spider_jobid == None:
            raise logging.error(u"name_spider或spider_jobid 不能为空!!!")
        self.conf = fileconfig(name_spider)
        self.allowed_domains = [self.conf.get("allowed_domains", "")]

        self.start_urls = []
        if self.conf.get("proxy").lower() in "false":
            self.proxy = False
        else:
            self.proxy = True

        rules = json.loads(self.conf.get("rules"))
        if rules.get("rules", "") == "":
            raise logging.error(u"规则解析未得到!!!")

    # 内容解析
    def parse(self, response):
        item = Item()
        sel = Selector(response)
        fields = json.loads(self.conf.get("fields"))
        rules = json.loads(self.conf.get("rules"))
        loops = rules.get("rules").get("rules_listxpath")
        if fields.get("fields", "") == "":
            logging.error(u"内容解析未得到!!!")
            yield item
        item.fields["url"] = Field()
        item.fields["spider_jobid"] = Field()
        item["spider_jobid"] = self.spider_jobid
        item.fields['word'] = Field()
        item['word'] = response.meta.get("word")
        # 加载动态库字段建立Field,xpath规则 (方法一)
        for loop in sel.xpath("{}".format(loops)):
            item['url'] = loop.xpath("./h3/a/@href").extract()
            for k in loadMySQL(self.conf.get("spider_name")):
                if fields.get("fields").get(k[2]) != None:
                    item.fields[k[2]] = Field()
                    if fields.get("fields").get(k[2]).keys()[0] == "xpath":
                        item[k[2]] = loop.xpath(u"{}".format(fields.get("fields").get(k[2]).get("xpath"))).extract()
                    elif fields.get("fields").get(k[2]).keys()[0] == "value":
                        item[k[2]] = u"{}".format(fields.get("fields").get(k[2]).get("value"))
            yield item
