# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:V1.0
@var:加载数据库配置信息
@note:加载数据库爬虫配置信息等

"""

import MySQLdb
import MySQLdb.cursors
import logging
import json
from xbzxproject.settings import BASECONFIG


# 加载规则配置文件
def fileconfig(name_spider):
    conf = loadscrapyconf()['mysql']
    try:
        conn = MySQLdb.connect(host=conf.get("host", "localhost"), port=conf.get("port", 3306),
                               user=conf.get("user", "root"), passwd=conf.get("passwd", "root"),
                               db=conf.get("databases"), charset=u"utf8", cursorclass=MySQLdb.cursors.DictCursor)
        cur = conn.cursor()
        cur.execute(u"SELECT * FROM net_spider WHERE spider_name='{}'".format(name_spider))
        try:
            keywords = cur.fetchall()[0]
        except:
            print u"爬虫名:{}".format(name_spider)
            raise logging.error(u"爬虫名:{} 配置信息未找到!".format(name_spider))
    except MySQLdb.Error, e:
        cur.close()
        conn.close()
        raise logging.error(u"Mysql Error %d: %s" % (e.args[0], e.args[1]))

    cur.close()
    conn.close()
    return keywords


# 读取自动建库字段
def loadMySQL(spider_name):
    conf = loadscrapyconf()['mysql']
    conn = MySQLdb.connect(host=conf.get("host", "localhost"), port=conf.get("port", 3306),
                           user=conf.get("user", "root"), passwd=conf.get("passwd", "root"),
                           db=conf.get("databases"), charset="utf8")
    cur = conn.cursor()
    cur.execute(u"SELECT gen_gendbtable_id FROM net_spider WHERE spider_name='{}'".format(spider_name))
    try:
        key = cur.fetchall()[0][0]
    except:
        raise logging.error(u"spider_type:{} 未找到,请检查爬虫类型!".format(spider_name))
    try:
        cur.execute(
            u"SELECT * FROM net_gendbtable_column WHERE gen_gendbtable_id = '{}'".format(key))
    except MySQLdb.Error, e:
        raise logging.error(u"Mysql Error %d: %s" % (e.args[0], e.args[1]))
    key = cur.fetchall()
    cur.close()
    conn.close()
    return key


# 加载初始化配置
def loadscrapyconf():
    return BASECONFIG


# 获取关键字
def loadkeywords():
    keywords = []
    conf = loadscrapyconf()['mysql']
    conn = MySQLdb.connect(host=conf.get("host", "localhost"), port=conf.get("port", 3306),
                           user=conf.get("user", "root"), passwd=conf.get("passwd", "root"),
                           db=conf.get("databases"), charset="utf8")
    cur = conn.cursor()
    cur.execute(u"SELECT keyword FROM  net_spider_keyword;")
    word = cur.fetchall()
    for keyword in word:
        keywords.append("".join(keyword))
    return keywords


if __name__ == "__main__":
    pass
    # conf = fileconfig('baidusearch')
    # rules = json.loads(conf.get("rules"))
    # loops = rules.get("rules").get("rules_listxpath")
    # fields = json.loads(conf.get("fields"))
    # print fields
    # for k in loadMySQL("baidusearch"):
    #     print k[2]
    #     if fields.get("fields").get(k[2]) != None:
    #         pass
