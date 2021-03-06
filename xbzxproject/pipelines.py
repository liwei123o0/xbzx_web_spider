# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:V1.0
@var:采集数据处理
@note:爬虫采集数据加工、处理、入库

"""

import logging
import re
import sys

import MySQLdb

from xbzxproject.utils import date_parse
from xbzxproject.utils.loadconfig import loadscrapyconf

reload(sys)
sys.setdefaultencoding("utf8")

# mysql入库Pipeline
class XbzxprojectPipeline(object):
    # 开启爬虫初始化工作
    conf = loadscrapyconf()['mysql']

    def open_spider(self, spider):
        self.cout = 1
        self.conn = MySQLdb.connect(host=self.conf.get("host", "localhost"), port=self.conf.get("port", 3306),
                                    user=self.conf.get("user", "root"), passwd=self.conf.get("passwd", "root"),
                                    db=self.conf.get("databases"), charset=u"utf8")
        self.cur = self.conn.cursor()
        # debug 模式
        if spider.debug:
            self.cur.execute("TRUNCATE net_spider_temp")
            self.conn.commit()
        logging.info(u"mysql连接成功!")
        logging.info(u"代理状态:%s" % spider.proxy)

    def process_item(self, item, spider):

        for k in item:
            item[k] = u"".join(item[k])
            item[k] = re.sub(r"\xa0", "", item[k])
            item[k] = re.sub(r"\u200b", "", item[k])
            item[k] = re.sub(r"\xa5", "", item[k])
            item[k] = re.sub(r"\u2022", "", item[k])
        try:
            # 判断字段是否存在
            if 'pubtime' in item:
                item['pubtime'] = unicode(date_parse.parse_date(item['pubtime']))
        except:
            logging.error(u"时间格式化错误!")
            return item
        # 收集item字段名及值
        fields = []
        values = []

        # 显示采集字段及内容
        for k, v in item.iteritems():
            fields.append(k)
            values.append(v)
        # debug为true时,数据入库!
        if spider.debug:
            print u"{:=^30}".format(self.cout)
            for k, v in item.iteritems():
                try:
                    print u"{:>13.13}:{}".format(k, v)
                except:
                    pass
            self.cur.execute(
                u"SELECT gen_gendbtable_id FROM net_spider WHERE spider_name='{}';".format(spider.name_spider))
            gen_gendbtable_id = self.cur.fetchall()[0][0]
            self.cur.execute(
                u"SELECT name,comments FROM  net_gendbtable_column WHERE gen_gendbtable_id='{}';".format(
                    gen_gendbtable_id))
            # 获取字段对照名
            datanames = dict(self.cur.fetchall())
            # 获取item的keys值
            keys = item.keys()
            kcout = 0
            data = ''
            for key in keys:
                kcout += 1
                comments = datanames.get(key, None)
                if comments is None:
                    continue
                data += '"%s":"%s"' % (comments, item[key]) + ","
            data = "{" + data + "}"
            data = data.replace(",}", "}")
            try:
                self.cur.execute(
                    u"INSERT INTO net_spider_temp(url,name_spider,spider_data) VALUES('%s','%s','%s');" % (item[u'url'],
                                                                                                           spider.name_spider,
                                                                                                           data))
                self.conn.commit()
            except MySQLdb.Error, e:
                logging.error(u"Mysql Error %d: %s" % (e.args[0], e.args[1]))
        else:
            try:
                # 通过爬虫名称找表明
                self.cur.execute(
                    u"SELECT  id,tablename FROM net_spider WHERE  spider_name='{}';".format(
                        spider.name_spider))
                TableName = self.cur.fetchall()
                if TableName:
                    net_spider_id = TableName[0][0]
                    TableName = TableName[0][1]

                    # 添加net_spider爬虫id
                    fields.append("net_spider_id")
                    values.append(net_spider_id)

                    # 根据 item 字段插入数据
                    sql = u"INSERT INTO {}({}) VALUES ( ".format(TableName, u",".join(fields))
                    for value in values:
                        sql += u"'{}',".format(MySQLdb.escape_string(value))
                    sql += u" ) ON DUPLICATE KEY UPDATE "
                    sql = sql.replace(u", ) ON DUPLICATE KEY UPDATE", u" ) ON DUPLICATE KEY UPDATE")
                    # sql = str(sql[0])
                    # 插入数据如果数据重复则更新已有数据
                    for f in fields:
                        sql += u'{}=VALUES({}),'.format(f, f)
                    sql = sql[:-1] + u',is_sync_index=0;'



                    self.cur.execute(sql)
                    self.conn.commit()

                    logging.info(u"数据插入/更新成功!")
                else:
                    logging.error(u"未对该爬虫创建数据库表!")
            except MySQLdb.Error, e:
                logging.error(u"Mysql Error %d: %s" % (e.args[0], e.args[1]))

        self.cout += 1
        return item

    # 关闭爬虫初始化工作
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
        logging.info(u"mysql关闭成功")
