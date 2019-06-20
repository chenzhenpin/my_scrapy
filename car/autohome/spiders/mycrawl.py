# -*- coding: utf-8 -*-
import re

import scrapy

from scrapy.http import Request
from autohome.items import AutohomeItem
from bs4 import BeautifulSoup

class MycrawlSpider(scrapy.Spider):
    name = 'carcrawl'
    allowed_domains = ['autohome.com.cn','https://www.autohome.com','www.autohome.com.cn']

    def start_requests(self):
        print('start------------------------------')
        # yield  Request("http://127.0.0.1:5000")
        yield Request("https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1%20&brandId=0%20&fctId=0%20&seriesId=0",
                      headers={
                        ":authority": "car.autohome.com.cn",
                        ":method":"GET",
                        ":path": "/price/brand-117-0-3-1.html",
                        ":scheme": "https",
                        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                        "accept-encoding":"gzip, deflate, br",
                        "accept-language":"zh-CN,zh;q=0.9",
                        "cache-control": "no-cache",
                        "cookie": "fvlid=1559528547310kVR9hHgWpy; sessionip=150.255.111.191; sessionid=663EF586-0CBD-449E-9C70-B34269FD320E%7C%7C2019-06-03+10%3A22%3A30.573%7C%7Cwww.baidu.com; autoid=4ad6df189969e9fc578ef1e533f0c53b; area=460106; ahpau=1; sessionuid=663EF586-0CBD-449E-9C70-B34269FD320E%7C%7C2019-06-03+10%3A22%3A30.573%7C%7Cwww.baidu.com; cookieCityId=110100; sessionvid=55DA4A1B-4D34-431D-B11E-7AE5D442BCF2; Hm_lvt_9924a05a5a75caf05dbbfb51af638b07=1559528572,1559542638; __utma=1.387912574.1559542991.1559542991.1559542991.1; __utmc=1; __utmz=1.1559542991.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __ah_uuid_ng=u_21235361; ahsids=3895_3825_2097_68_67_3349; ahpvno=117; Hm_lpvt_9924a05a5a75caf05dbbfb51af638b07=1559547405; ref=www.baidu.com%7C0%7C0%7C0%7C2019-06-03+15%3A36%3A50.463%7C2019-06-03+10%3A22%3A30.573; ahrlid=1559547404780sCsFsHLW5t-1559547412160",
                        "pragma": "no-cache",
                        "upgrade-insecure-requests": "1",
                        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"

                      })

    def parse(self, response):
        print("parse----------------")
        item=AutohomeItem()
        context=str(response.body,"gbk")
        body=context[18:-3]
        soup =BeautifulSoup(body)
        initialsNames=soup.find_all('div', class_="cartree-letter")
        uElemts = soup.find_all('ul')
        for index,uElemt in enumerate(uElemts,0):
            liElents=uElemt.find_all('li')
            for liElent in liElents:
                item["initialsName"] = initialsNames[index].get_text()
                brandName= liElent.find('h3').find('a').get_text()
                item["brandName"] = brandName[0:brandName.find("(")]
                item["brandUrl"]= liElent.find('h3').a['href']
                item["brandId"]=liElent.attrs["id"]
                yield item



