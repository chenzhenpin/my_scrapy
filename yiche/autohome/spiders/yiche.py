# -*- coding: utf-8 -*-
import re

import scrapy

from scrapy.http import Request
from autohome.items import AutohomeItem
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import time
import pymysql
import requests
import os
class MycrawlSpider(scrapy.Spider):
    name = 'yiche'
    allowed_domains = ['http://car.bitauto.com/','http://car.bitauto.com/','http://car.bitauto.com/']

    def __init__(self):
        try:
            self.conn = pymysql.connect(host="127.0.0.1", user="root", passwd="333333", db="yiche", charset="utf8")
            self.brandCode = 100
        except Exception as e:
            print(r'error connect--------------------------------------------------')

    def start_requests(self):
        print('--------------')
        driver = webdriver.Firefox()
        driver.get("http://car.bitauto.com/")
        time.sleep(2)
        divs=driver.find_elements_by_xpath('//*[@id="treeNav"]/div[2]/div')
        context=""
        for div in divs:
            context=div.get_attribute('innerHTML')


        soup = BeautifulSoup(context)
        initialsLis = soup.find('div', class_='tree-list').find('ul', class_="list-con").find_all('li',id=re.compile("letter*"))
        for initialsLi in initialsLis:

            initialsName= initialsLi.find('div', class_='num-tit').get_text()
            brandLis = initialsLi.find('ul', class_='brand-list').find_all('li')
            for brandLi in brandLis:
                brandLink = brandLi.a['href']
                logoUrl= brandLi.find('a',class_='mainBrand').find('span').img['src']
                brandName= brandLi.find('a',class_='mainBrand').find('div',class_='brand-name').find('span').get_text()
                self.brandCode=self.brandCode+1
                path=self.download(logoUrl)
                now=datetime.datetime.now()
                sql = "INSERT INTO sys_dictionary_data (fk_dictionary, dictdata_name, dictdata_value, remark, create_date, is_enable) VALUES ( %s, %s, %s, %s, %s, %s);"
                cur = self.conn.cursor()
                cur.execute(sql, ('2a7c09c5-30d7-11e8-a6cd-1051721b40df',brandName,str(self.brandCode),path,now,'T'))
                self.conn.commit()
                yield Request("http://car.bitauto.com/"+brandLink,
                        headers={
                        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                        "accept-encoding":"gzip, deflate, br",
                        "accept-language":"zh-CN,zh;q=0.9",
                        "cache-control": "no-cache",
                        "cookie": "fvlid=1559528547310kVR9hHgWpy; sessionip=150.255.111.191; sessionid=663EF586-0CBD-449E-9C70-B34269FD320E%7C%7C2019-06-03+10%3A22%3A30.573%7C%7Cwww.baidu.com; autoid=4ad6df189969e9fc578ef1e533f0c53b; area=460106; ahpau=1; sessionuid=663EF586-0CBD-449E-9C70-B34269FD320E%7C%7C2019-06-03+10%3A22%3A30.573%7C%7Cwww.baidu.com; cookieCityId=110100; sessionvid=55DA4A1B-4D34-431D-B11E-7AE5D442BCF2; Hm_lvt_9924a05a5a75caf05dbbfb51af638b07=1559528572,1559542638; __utma=1.387912574.1559542991.1559542991.1559542991.1; __utmc=1; __utmz=1.1559542991.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __ah_uuid_ng=u_21235361; ahsids=3895_3825_2097_68_67_3349; ahpvno=117; Hm_lpvt_9924a05a5a75caf05dbbfb51af638b07=1559547405; ref=www.baidu.com%7C0%7C0%7C0%7C2019-06-03+15%3A36%3A50.463%7C2019-06-03+10%3A22%3A30.573; ahrlid=1559547404780sCsFsHLW5t-1559547412160",
                        "pragma": "no-cache",
                        "upgrade-insecure-requests": "1",
                        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"

                    }
                ,callback=lambda response,initialsName=initialsName,logoUrl=logoUrl,brandName=brandName,brandCode=self.brandCode:self.parse(response,initialsName,logoUrl,brandName,brandCode))

    def parse(self, response,initialsName,logoUrl,brandName,brandCode):
        print("parse----------------")

        # item["initialsName"]=ytem["initialsName"]
        # item["logoUrl"]=ytem["logoUrl"]
        # item["brandName"]= ytem["brandName"]
        body = str(response.body,"utf-8")
        bodyElem = BeautifulSoup(body)
        maindiv=bodyElem.find('div',class_='main-inner-section condition-selectcar type-3')
        modelblock=maindiv.find('div',id='divCsLevel_0')
        models=modelblock.find_all('div',class_="row block-4col-180")
        for classblock in models:
            classmodels=classblock.find_all('div',class_='col-xs-3')
            for model in classmodels:
                item = AutohomeItem()
                item["initialsName"]=initialsName
                item["logoUrl"]=logoUrl
                item["brandName"]=brandName
                item["brandCode"]=brandCode
                item["modelUrl"]=model.find('div',class_='img').a["href"]
                item["modelName"]=model.find('div',class_='img').a["title"]
                item["modelImgUrl"]=model.find('div',class_='img').find('a').img['src']
                yield item

    def download(self, link):
        filename = str(self.brandCode)+re.findall(r'.*/(.+)', link)[0]
        try:
            pic = requests.get(link)
            imgPath="D:\carinfo\logo" + os.sep +filename
            if pic.status_code == 200:
                with open(imgPath, 'wb') as fp:
                    fp.write(pic.content)
                    fp.close()
            return "/uploads/carinfo/logo/"+filename
        except Exception as e:
            print(e)
            print("保存失败>>"+filename)

