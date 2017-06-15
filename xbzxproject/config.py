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
import ConfigParser

conf = ConfigParser.SafeConfigParser()

conf.read("../settings.conf")

print conf.sections()
print conf.options('scrapyd')
print conf.get('scrapyd', 'host')
