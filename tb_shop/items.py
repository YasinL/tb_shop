# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class JdpcItem(scrapy.Item):
    # 商品信息
    shop_id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    brand = scrapy.Field()
    brand_url = scrapy.Field()
    zy = scrapy.Field()
    price = scrapy.Field()

    fl1 = scrapy.Field()
    fl1_url = scrapy.Field()
    fl2 = scrapy.Field()
    fl3 = scrapy.Field()



    def get_insert_sql(self):
        shop_id = self["shop_id"]
        url = self["url"]
        title = self["title"]
        brand = self["brand"]
        brand_url = self["brand_url"]
        zy = self["zy"]
        price = self["price"]

        fl1 = self["fl1"]
        fl1_url = self["fl1_url"]
        fl2 = self["fl2"]
        fl3 = self["fl3"]

        try:
            insert_sql = """
                           insert into JDAll(shop_id,url,title,brand,brand_url,zy,price,fl1,fl1_url,fl2,fl3)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                       """
            params = (
            shop_id,url, title, brand, brand_url, zy, price, fl1, fl1_url, fl2, fl3)
            print("return SQL 语句")
            return insert_sql, params
        except BaseException as e:
            print("数据插入异常 error %s" %e)
