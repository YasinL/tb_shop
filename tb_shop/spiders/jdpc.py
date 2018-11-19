# -*- coding: utf-8 -*-
import scrapy

#
# class JdSpider(scrapy.Spider):
#     name = 'jd'
#     allowed_domains = ['jdsp']
#     start_urls = ['http://jdsp/']
#
#     def parse(self, response):
#         pass

import os,sys
import scrapy
import json
import requests
from scrapy_splash import SplashRequest
from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import Rule,CrawlSpider
# from scrapy.spiders.splashcrawl  import Rule,CrawlSpider
from scrapy_redis.spiders import RedisSpider
# from ArticleSpider.items import JDAllItem
from jdpc.items import JdpcItem

lua_script = """
function main(splash)
    splash:go(splash.args.url)
    splash:wait(0.5)
    return splash:html()
end
"""
urllist = ["https://list.jd.com/list.html?cat=39,842,229","https://list.jd.com/list.html?cat=696,629,6850","https://list.jd.com/list.html?cat=38,202,203","https://list.jd.com/list.html?cat=38,202,9766","https://list.jd.com/list.html?cat=38,463,487","https://list.jd.com/list.html?cat=38,202,208","https://list.jd.com/list.html?cat=38,2099,9768","https://list.jd.com/list.html?cat=672,265,937","https://list.jd.com/list.html?cat=36,38,3544","https://list.jd.com/list.html?cat=36,387,427","https://list.jd.com/list.html?cat=672,2599,2078","https://list.jd.com/list.html?cat=36,387,429","https://list.jd.com/list.html?cat=36,387,420","https://list.jd.com/list.html?cat=36,387,42","https://list.jd.com/list.html?cat=36,383,404","https://list.jd.com/list.html?cat=36,38,39","https://list.jd.com/list.html?cat=36,38,392","https://list.jd.com/list.html?cat=36,38,389","https://list.jd.com/list.html?cat=36,383,394","https://list.jd.com/list.html?cat=36,383,355","https://list.jd.com/list.html?cat=36,38,547","https://list.jd.com/list.html?cat=36,38,3546","https://list.jd.com/list.html?cat=36,387,424","https://list.jd.com/list.html?cat=737,277,4934","https://list.jd.com/list.html?cat=36,38,389","https://list.jd.com/list.html?cat=38,462,245","https://list.jd.com/list.html?cat=39,4997,3292","https://list.jd.com/list.html?cat=35,346,2028","https://list.jd.com/list.html?cat=36,38,560","https://list.jd.com/list.html?cat=36,387,49","https://list.jd.com/list.html?cat=36,387,428","https://list.jd.com/list.html?cat=36,386,3550","https://list.jd.com/list.html?cat=36,387,423","https://list.jd.com/list.html?cat=620,58,968","https://list.jd.com/list.html?cat=36,383,563","https://list.jd.com/list.html?cat=36,387,932","https://list.jd.com/list.html?cat=6728,6745,6785","https://list.jd.com/list.html?cat=36,384,406","https://list.jd.com/list.html?cat=39,526,553","https://list.jd.com/list.html?cat=36,384,405","https://list.jd.com/list.html?cat=36,38,393","https://list.jd.com/list.html?cat=36,386,42","https://list.jd.com/list.html?cat=737,276,74","https://list.jd.com/list.html?cat=36,383,398","https://list.jd.com/list.html?cat=36,386,923","https://list.jd.com/list.html?cat=6994,700","https://list.jd.com/list.html?cat=39,527,555","https://list.jd.com/list.html?cat=36,383,548","https://list.jd.com/list.html?cat=36,383,397","https://list.jd.com/list.html?cat=36,386,922","https://list.jd.com/list.html?cat=36,385,408","https://list.jd.com/list.html?cat=36,385,409","https://list.jd.com/list.html?cat=36,385,550","https://list.jd.com/list.html?cat=38,2628,236","https://list.jd.com/list.html?cat=737,276,742","https://list.jd.com/list.html?cat=729,73,9780","https://list.jd.com/list.html?cat=38,2099,9759","https://list.jd.com/list.html?cat=729,730,6908","https://list.jd.com/list.html?cat=729,73,696","https://list.jd.com/list.html?cat=38,2099,9754","https://list.jd.com/list.html?cat=38,2628,238","https://list.jd.com/list.html?cat=672,265,934","https://list.jd.com/list.html?cat=39,842,229","https://list.jd.com/list.html?cat=38,2628,237","https://list.jd.com/list.html?cat=729,73,9780","https://list.jd.com/list.html?cat=38,2628,240","https://list.jd.com/list.html?cat=729,73,2062","https://list.jd.com/list.html?cat=729,730,6907","https://list.jd.com/list.html?cat=729,73,206","https://list.jd.com/list.html?cat=38,2099,9760","https://list.jd.com/list.html?cat=39,842,230","https://list.jd.com/list.html?cat=38,2099,9756","https://list.jd.com/list.html?cat=729,73,9778","https://list.jd.com/list.html?cat=729,730,6909","https://list.jd.com/list.html?cat=729,73,697","https://list.jd.com/list.html?cat=39,842,232","https://list.jd.com/list.html?cat=38,2099,9757","https://list.jd.com/list.html?cat=729,730,978","https://list.jd.com/list.html?cat=39,842,233","https://list.jd.com/list.html?cat=729,730,2067","https://list.jd.com/list.html?cat=38,2628,239","https://list.jd.com/list.html?cat=729,73,9772","https://list.jd.com/list.html?cat=729,730,9783","https://list.jd.com/list.html?cat=729,73,9774","https://list.jd.com/list.html?cat=38,2099,9755","https://list.jd.com/list.html?cat=729,730,2068","https://list.jd.com/list.html?cat=38,2628,234","https://list.jd.com/list.html?cat=729,73,694","https://list.jd.com/list.html?cat=729,730,690","https://list.jd.com/list.html?cat=729,73,698","https://list.jd.com/list.html?cat=38,2099,200","https://list.jd.com/list.html?cat=39,842,226","https://list.jd.com/list.html?cat=38,2628,226","https://list.jd.com/list.html?cat=35,343,3983","https://list.jd.com/list.html?cat=35,342,3982","https://list.jd.com/list.html?cat=38,202,204","https://list.jd.com/list.html?cat=39,633,634","https://list.jd.com/list.html?cat=652,98,982","https://list.jd.com/list.html?cat=670,703,0969","https://list.jd.com/list.html?cat=35,342,9738","https://list.jd.com/list.html?cat=35,342,973","https://list.jd.com/list.html?cat=35,345,37","https://list.jd.com/list.html?cat=6728,3256,3257","https://list.jd.com/list.html?cat=38,25,220","https://list.jd.com/list.html?cat=38,202,206","https://list.jd.com/list.html?cat=39,842,227","https://list.jd.com/list.html?cat=35,343,9705","https://list.jd.com/list.html?cat=35,342,9724","https://list.jd.com/list.html?cat=38,202,9762","https://list.jd.com/list.html?cat=39,842,228","https://list.jd.com/list.html?cat=35,343,996","https://list.jd.com/list.html?cat=38,2628,233","https://list.jd.com/list.html?cat=670,703,009","https://list.jd.com/list.html?cat=38,202,207","https://list.jd.com/list.html?cat=38,2628,225","https://list.jd.com/list.html?cat=39,842,843","https://list.jd.com/list.html?cat=35,3529,3530","https://list.jd.com/list.html?cat=670,67,674","https://list.jd.com/list.html?cat=672,265,988","https://list.jd.com/list.html?cat=39,4997,4999","https://list.jd.com/list.html?cat=35,343,989","https://list.jd.com/list.html?cat=35,342,9726","https://list.jd.com/list.html?cat=35,343,999","https://list.jd.com/list.html?cat=35,342,2089","https://list.jd.com/list.html?cat=35,343,973","https://list.jd.com/list.html?cat=38,202,9764","https://list.jd.com/list.html?cat=38,202,205","https://list.jd.com/list.html?cat=35,343,985","https://list.jd.com/list.html?cat=35,345,204","https://list.jd.com/list.html?cat=35,343,354","https://list.jd.com/list.html?cat=35,342,348","https://list.jd.com/list.html?cat=35,342,9733","https://list.jd.com/list.html?cat=35,345,9753","https://list.jd.com/list.html?cat=39,633,234","https://list.jd.com/list.html?cat=36,625,662","https://list.jd.com/list.html?cat=38,2628,227","https://list.jd.com/list.html?cat=39,527,557","https://list.jd.com/list.html?cat=737,794,880","https://list.jd.com/list.html?cat=38,202,9764","https://list.jd.com/list.html?cat=35,343,970","https://list.jd.com/list.html?cat=35,342,9732","https://list.jd.com/list.html?cat=39,526,3286","https://list.jd.com/list.html?cat=38,2628,224","https://list.jd.com/list.html?cat=35,345,37","https://list.jd.com/list.html?cat=39,842,223","https://list.jd.com/list.html?cat=38,2628,229","https://list.jd.com/list.html?cat=35,345,205","https://list.jd.com/list.html?cat=35,345,368","https://list.jd.com/list.html?cat=35,345,2006","https://list.jd.com/list.html?cat=38,254,258","https://list.jd.com/list.html?cat=35,345,202","https://list.jd.com/list.html?cat=39,842,227","https://list.jd.com/list.html?cat=38,254,259","https://list.jd.com/list.html?cat=644,682,3069","https://list.jd.com/list.html?cat=35,343,9706","https://list.jd.com/list.html?cat=35,342,9729","https://list.jd.com/list.html?cat=35,343,979","https://list.jd.com/list.html?cat=38,202,9763","https://list.jd.com/list.html?cat=38,2628,23","https://list.jd.com/list.html?cat=38,2628,232","https://list.jd.com/list.html?cat=737,738,2395","https://list.jd.com/list.html?cat=35,343,9708","https://list.jd.com/list.html?cat=35,342,9728","https://list.jd.com/list.html?cat=35,343,998","https://list.jd.com/list.html?cat=35,342,9725","https://list.jd.com/list.html?cat=35,345,20","https://list.jd.com/list.html?cat=38,2628,223","https://list.jd.com/list.html?cat=6728,6745,6798","https://list.jd.com/list.html?cat=35,345,369","https://list.jd.com/list.html?cat=35,345,2008","https://list.jd.com/list.html?cat=39,4997,7062","https://list.jd.com/list.html?cat=35,345,364","https://list.jd.com/list.html?cat=35,345,2009","https://list.jd.com/list.html?cat=38,254,256","https://list.jd.com/list.html?cat=39,633,635","https://list.jd.com/list.html?cat=35,346,2023","https://list.jd.com/list.html?cat=35,346,376","https://list.jd.com/list.html?cat=35,346,9793","https://list.jd.com/list.html?cat=35,346,2025","https://list.jd.com/list.html?cat=35,346,2024","https://list.jd.com/list.html?cat=35,346,9792","https://list.jd.com/list.html?cat=38,2099,9768","https://list.jd.com/list.html?cat=38,254,257","https://list.jd.com/list.html?cat=672,2575,2069","https://list.jd.com/list.html?cat=672,2576,2073","https://list.jd.com/list.html?cat=672,2577,2076","https://list.jd.com/list.html?cat=672,2577,3998","https://list.jd.com/list.html?cat=672,2575,5260","https://list.jd.com/list.html?cat=672,265,986","https://list.jd.com/list.html?cat=652,829,847","https://list.jd.com/list.html?cat=672,2577,2074","https://list.jd.com/list.html?cat=672,2575,5258","https://list.jd.com/list.html?cat=672,2576,207","https://list.jd.com/list.html?cat=672,2577,5265","https://list.jd.com/list.html?cat=672,2575,5259","https://list.jd.com/list.html?cat=672,2575,5256","https://list.jd.com/list.html?cat=672,2576,455","https://list.jd.com/list.html?cat=672,2575,2580","https://list.jd.com/list.html?cat=672,265,987","https://list.jd.com/list.html?cat=672,2576,5262","https://list.jd.com/list.html?cat=672,2576,2584","https://list.jd.com/list.html?cat=737,752,899","https://list.jd.com/list.html?cat=2379,3302,333","https://list.jd.com/list.html?cat=39,4997,5002","https://list.jd.com/list.html?cat=672,2577,527","https://list.jd.com/list.html?cat=672,2577,2588","https://list.jd.com/list.html?cat=672,2577,3543","https://list.jd.com/list.html?cat=672,2576,3542","https://list.jd.com/list.html?cat=672,2575,2070","https://list.jd.com/list.html?cat=35,346,2036","https://list.jd.com/list.html?cat=38,247,252","https://list.jd.com/list.html?cat=672,2577,3997","https://list.jd.com/list.html?cat=672,2577,2587","https://list.jd.com/list.html?cat=672,2575,5257","https://list.jd.com/list.html?cat=672,2576,2072","https://list.jd.com/list.html?cat=38,462,472","https://list.jd.com/list.html?cat=39,525,548","https://list.jd.com/list.html?cat=36,385,408","https://list.jd.com/list.html?cat=35,346,376","https://list.jd.com/list.html?cat=35,346,202","https://list.jd.com/list.html?cat=35,346,2022","https://list.jd.com/list.html?cat=620,62,634","https://list.jd.com/list.html?cat=6728,6743,3254","https://list.jd.com/list.html?cat=39,4997,639","https://list.jd.com/list.html?cat=737,752,2397","https://list.jd.com/list.html?cat=320,2202,22",]


class JdSpider(RedisSpider):
    name = "jdid"
    redis_key = "jd:start_urls"
    allowed_domains = ["jd.com"]
    header = {
        'Host': 'club.jd.com',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
    }
    list_header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'list.jd.com',
        'If-Modified-Since': 'Mon, 22 Jan 2018 06:23:20 GMT',
        'Upgrade-Insecure-Requests': '1'
    }




    def parse(self,response):
        # 解析list链接
        pattern = "https://list\.jd\.com/list\.html\?cat=.*"
        le = LinkExtractor(allow=pattern)
        links = le.extract_links(response)
        # print("+++++++++ %s" % response)
        print("发现list页面共：【%s】" %len(links))
        print("eeeeeeeeee %s" % urllist )
        for i in links:
            print("-------------------->%s" %i)
            yield scrapy.Request(i,callback=self.next_page)
            #yield SplashRequest(i.url, endpoint='execute', args={'images': 0, 'lua_source': lua_script},cache_args=['lua_source'], callback=self.parse_shop)
    def next_page(self,response):
        # 获取page total
        page_total = int(response.css('span.fp-text i::text').extract_first())
        print("开始获取下一页")
        # print(response)
        print(page_total)
        for page in range(2,page_total + 1):
            print("第几页:%s" %page)
            page_url = "%s&page=%s" %(response.url,page)
            print("获取list：【%s】，第【%s】页。"%(response.url, page))
            return SplashRequest(page_url, args={'wait': 2, 'images': 0}, callback=self.parse_shop,splash_headers=self.header)
            # yield SplashRequest(page_url, endpoint='execute', args={'images': 0, 'lua_source': lua_script},cache_args=['lua_source'], callback=self.parse_shop,dont_filter=True)

    def fl(self,response):
        re_url =  response.url
        sel_fl_url = re_url.split("&")[0]
        sel_fl = sel_fl_url.xpath('.//div[@id="J_crumbsBar"]').xpath('.//div[@class="crumbs-nav"]')
        fl = sel_fl.css(".crumbs-nav-item  a::text").extract_first()
        fl = sel_fl.css(".crumbs-nav-item  a::text").extract_first()
        fl_url =  sel_fl.css(".crumbs-nav-item  a::attr('href')").extract_first()
        fl2 = sel_fl.css(".trigger span::text").extract_first()
        fl3 = sel_fl.css(".trigger span::text").extract_first()


        print(sel_fl.split("&")[0])

        return sel_fl.split("&")[0]


    def parse_shop(self, response):


        sel_fl = response.xpath('.//div[@id="J_crumbsBar"]').xpath('.//div[@class="crumbs-nav"]')
        fl1 = sel_fl.css(".crumbs-nav-item  a::text").extract_first()
        fl1_url =  sel_fl.css(".crumbs-nav-item  a::attr('href')").extract_first()
        fl2 = sel_fl.css(".trigger:nth-child(1) span::text").extract_first()
        fl3 = sel_fl.css(".trigger:nth-last-child(1) span::text").extract_first()


        sel_list = response.xpath('//div[@id="plist"]').xpath('.//li[@class="gl-item"]')
        for sel in sel_list:
            print("开始解析list页面，商品信息")
            url = "http:%s" %sel.css(".p-name a::attr('href')").extract_first()
            shop_id = url.split("/")[-1].split(".")[0]
            title = sel.css(".p-name a em::text").extract_first().strip("\n").strip(" ")
            brand = sel.css(".p-shop span a::attr('title')").extract_first()
            brand_url = sel.css(".p-shop span a::attr('href')").extract_first()
            zy = sel.css(".p-icons i::text").extract_first()
            price = sel.css(".p-price strong i::text").extract_first()
            session = requests.Session()


            print("开始解析商品")
            # shop_id = response.meta.get("shop_id")
            # url = response.meta.get("url")
            # title = response.meta.get("title")
            # brand = response.meta.get("brand")
            # brand_url = response.meta.get("brand_url")
            # price = response.meta.get("price")

            JDItem = JdpcItem()
            # JDItem=dict(shop_id=shop_id,url=url,title=title,brand=brand,brand_url=brand_url,price=price)

            JDItem["shop_id"] = shop_id
            JDItem["url"] = url
            JDItem["title"] = title
            JDItem["brand"] = brand
            JDItem["brand_url"] = brand_url
            JDItem["zy"] = zy
            JDItem["price"] = price

            JDItem["fl1"] = fl1
            JDItem["fl1_url"] = fl1_url
            JDItem["fl2"] = fl2
            JDItem["fl3"] = fl3

            print("yield商品")
            print(JdpcItem)
            print(JDItem["shop_id"])
            print(price)

            print(fl1)
            print(fl1_url)
            print(fl2)
            print(fl3)

            yield JDItem
            # yield scrapy.Request(meta=shop_info,headers=self.header,callback=self.parse_comment)


if __name__ == '__main__':
    print(len(urllist))
    # def ni():
    #     # 解析list链接
    #     pattern = "https://list\.jd\.com/list\.html\?cat=.*"
    #     le = LinkExtractor(allow=pattern)
    #     links = le.extract_links(re)
    #
    #     print("发现list页面共：【%s】" %len(links))
    #     for i in links:
    #         print("-------------------->%s" %i.url)
    #         # yield scrapy.Request(i.url,callback=self.next_page)
    # ni()
    # def parse_comment(self,response):
    #     print("开始解析评价")
    #     shop_id = response.meta.get("shop_id")
    #     url = response.meta.get("url")
    #     title = response.meta.get("title")
    #     brand = response.meta.get("brand")
    #     brand_url = response.meta.get("brand_url")
    #     price = response.meta.get("price")
    #
    #     JDItem = JdpcItem()
    #
    #     JDItem["shop_id"] = shop_id
    #     JDItem["url"] = url
    #     JDItem["title"] = title
    #     JDItem["brand"] = brand
    #     JDItem["brand_url"] = brand_url
    #     JDItem["price"] = price
    #
    #     print("yield评价")
    #     yield JdpcItem
