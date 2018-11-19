#!/usr/bin/env python
# -*- coding:utf-8 -*-
__Author__ = "Yasin Li"

from scrapy import cmdline

# cmdline.execute("scrapy crawl jdpc".split())
cmdline.execute(["scrapy","crawl","tb_shop","-s", "LOG_LEVEL=DEBUG"])
