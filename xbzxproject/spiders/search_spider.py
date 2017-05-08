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
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider, Rule
from xbzxproject.utils.loadconfig import loadMySQL, fileconfig, loadkeywords
import logging
import json
from scrapy.selector import Selector
from scrapy.http import Request


class SearchSpider(CrawlSpider):
    name = "search"

    # 加载规则配置文件
    # 获取额外参数
    def __init__(self, spider_jobid=None, name_spider=None, debug=False, *args, **kwargs):
        self.spider_jobid = spider_jobid
        self.name_spider = name_spider
        self.debug = debug
        self.loadconf(name_spider, spider_jobid)
        super(SearchSpider, self).__init__(*args, **kwargs)

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

        search = False
        if search:
            keywords = loadkeywords()
        else:
            keywords = [u'雷雷 格斗狂人,打假,PK', u'霍金,地球,离开']

        for word in keywords:
            self.start_urls.append(self.conf.get("start_urls", "").format(word=word).replace(",", " "))
        keys = self.conf.get("search", "1")
        rules = json.loads(self.conf.get("rules"))
        if rules.get("rules", "") == "":
            logging.error(u"规则解析未得到!!!")
            return
        if keys == "1":
            for url in self.start_urls:
                Request(url, callback=self.parse)

        elif keys == "2":
            rules = json.loads(self.conf.get("rules"))
            if rules.get("rules", "") == "":
                logging.error(u"规则解析未得到!!!")
                return
            self.rules = [
                Rule(LinkExtractor(
                    restrict_xpaths=u"{}".format(rules.get("rules").get("reles_pagexpath"))),
                    follow=True,
                ),
                Rule(LinkExtractor(
                    restrict_xpaths=u"{}".format(rules.get("rules").get("rules_listxpath"))),
                    follow=False,
                    callback="parse_item")
            ]

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
        # 加载动态库字段建立Field,xpath规则 (方法一)
        for loop in sel.xpath("{}".format(loops)):
            item['url'] = loop.xpath("./h3/a/@href").extract()
            for k in loadMySQL(self.conf.get("spider_name")):
                if fields.get("fields").get(k[2]) != None:
                    item.fields[k[2]] = Field()
                    if fields.get("fields").get(k[2]).keys()[0] == "xpath":
                        item[k[2]] = loop.xpath(u"{}".format(fields.get("fields").get(k[2]).get("xpath"))).extract()
                    # if fields.get("fields").get(k[2]).keys()[0] == "xpath":
                    #     l.add_xpath(k[2], u"{}".format(fields.get("fields").get(k[2]).get("xpath")),
                    #                 MapCompose(unicode.strip))
                    elif fields.get("fields").get(k[2]).keys()[0] == "value":
                        item[k[2]] = u"{}".format(fields.get("fields").get(k[2]).get("value"))
                        #     l.add_value(k[2], u"{}".format(fields.get("fields").get(k[2]).get("value")))
            yield item

    # 内容解析
    def parse_item(self, response):
        item = Item()
        fields = json.loads(self.conf.get("fields"))
        l = ItemLoader(item, response)
        if fields.get("fields", "") == "":
            logging.error(u"内容解析未得到!!!")
            return l.load_item()
        item.fields["url"] = Field()
        item.fields["spider_jobid"] = Field()
        l.add_value("url", response.url)
        l.add_value("spider_jobid", self.spider_jobid)
        # 加载动态库字段建立Field,xpath规则 (方法一)
        for k in loadMySQL(self.conf.get("spider_name")):
            if fields.get("fields").get(k[2]) != None:
                item.fields[k[2]] = Field()
                if fields.get("fields").get(k[2]).keys()[0] == "xpath":
                    l.add_xpath(k[2], u"{}".format(fields.get("fields").get(k[2]).get("xpath")),
                                MapCompose(unicode.strip))
                elif fields.get("fields").get(k[2]).keys()[0] == "value":
                    l.add_value(k[2], u"{}".format(fields.get("fields").get(k[2]).get("value")))
        return l.load_item()
