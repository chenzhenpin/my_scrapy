# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AutohomeItem(scrapy.Item):
    # define the fields for your item here like:
    initialsName = scrapy.Field()
    logoUrl = scrapy.Field()
    brandName = scrapy.Field()
    modelName=scrapy.Field()
    modelImgUrl=scrapy.Field()
    modelUrl=scrapy.Field()
    brandCode=scrapy.Field()
