# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZmrenwuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    form_url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    from_url = scrapy.Field()


