# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from zmrenwu.items import ZmrenwuItem


class MyzmrenwuSpider(scrapy.Spider):
    name = "myzmrenwu"
    allowed_domains = ["zmrenwu.com"]
    start_urls = ['http://zmrenwu.com/post/2/']

    def parse(self, response):
        item = ZmrenwuItem()
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

        item["title"] = response.xpath("//article/h1/text()").extract()

        item["content"] = response.xpath("//div[@class='post-body top-gap-big']").extract()

        item['from_url']=response._url
        print('------------------')

        yield item

        for i in range(3, 50):
            url = "http://zmrenwu.com/post/"+ str(i)
            print(url)
            yield Request(url, callback=self.parse,errback=self.parse)
        return item

