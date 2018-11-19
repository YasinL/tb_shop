#!/usr/bin/env python
# -*- coding:utf-8 -*-
__Author__ = "Yasin Li"


import os,sys
import scrapy
import json
import requests
from scrapy_splash import SplashRequest
from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import Rule,CrawlSpider
# from scrapy.spiders.splashcrawl  import Rule,CrawlSpider
from scrapy_redis.spiders import RedisSpider

def parse(self, response):
    # 解析list链接
    pattern = "https://list\.jd\.com/list\.html\?cat=.*"
    # pattern = "https://list.jd.com/list.html?cat=1713,3273,3544"
    le = LinkExtractor(allow=pattern)
    links = le.extract_links(response)
    print("发现list页面共：【%s】" % len(links))



import  requests


url = "https://www.jd.com/allSort.aspx"
urlget = requests.get(url)

response = urlget.text
print(response)


