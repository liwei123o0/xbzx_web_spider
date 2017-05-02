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
import re
import datetime
import time

url = "http://search.51job.com/jobsearch/search_result.php?jobarea=200000&district=000000&funtype=0000&industrytype=00&issuedate=9&providesalary=99&keywordtype=1&curr_page={page}&lang=c&stype=1&postchannel=0000&workyear=99&cotype=99%C2%B0reefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&fromType=14&dibiaoid=0&confirmdate=9,"

for i in xrange(1, 2001, 1):
    print url.format(page=i)
