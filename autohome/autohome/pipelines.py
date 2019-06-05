# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

import  pymysql
import requests
from scrapy import Selector
from bs4 import BeautifulSoup
import re
import os
import traceback
import random
class AutohomePipeline(object):
    def __init__(self):
        try:
            self.conn = pymysql.connect(host="127.0.0.1", user="root", passwd="333333", db="my_scrapy", charset="utf8")
            self.myTotal=0
            self.startTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(r'error connect--------------------------------------------------')
            traceback.print_exc(e)

    def process_item(self, item, spider):
        link='https://car.autohome.com.cn' + item['brandUrl']
        urls=self.craw(item,link)
        for url in urls:
            self.craw(item, url)
        print("条数：" + str(self.myTotal))
        return item


    def craw(self,item,link):
        modelName = level = structure = price = motor = engine = transmission = chargingTime = advancePrice = subsidizedPrice = mileage = rating = imgUrl = imgPath = imgName = wcolor = brandName = sellStatus=None
        r = requests.get(link)
        liNavText = Selector(text=r.text).xpath('/html/body/div[2]/div/div[2]/div[7]/div/div[2]/div[1]/ul').get()
        liNavElemts = BeautifulSoup(liNavText).find_all('li')
        links = []
        for liNavElemt in liNavElemts:
            if liNavElemt['class']== ['current']:
                sellStatus = liNavElemt.get_text()
            elif liNavElemt['class'] == ['disabled']:
                continue
            else:
                try:
                    links.append('https://car.autohome.com.cn'+liNavElemt.a['href'])
                except Exception as e:
                    traceback.print_exc(e)

        brandtab = Selector(text=r.text).xpath('//*[@id="brandtab-1"]').get()
        soup = BeautifulSoup(brandtab)
        brandName = soup.find('div', class_='brand-title').find('h3').get_text()
        listCont = soup.find_all('div', class_='list-cont')

        for cont in listCont:
            self.myTotal = self.myTotal + 1

            modelName = cont.find('div', class_='main-title').find('a', class_="font-bold").get_text()
            rating_text = cont.find('div', class_='score-cont').get_text()
            try:
                ratingName, rating = rating_text.split("：")
            except Exception as e:
                traceback.print_exc(e)
            imgUrl = "https:" + cont.find('div', class_='list-cont-img').find('a').find('img')["src"]

            mainLeverRight=cont.find('div', class_='main-lever-right')
            if mainLeverRight:
                price_text = mainLeverRight.find('div').get_text()
                try:
                    priceName, priceValue = price_text.split("：")
                except Exception as e:
                    traceback.print_exc(e)
                if priceName == "预售价":
                    advancePrice = priceValue
                elif priceName == "指导价":
                    price = priceValue
            leftLis = cont.find('div', class_='main-lever-left').find('ul', class_='lever-ul').find_all('li')
            for li in leftLis:
                text = li.get_text()
                if "：" not in text:
                    continue
                try:
                    name, value = text.split("：")
                except Exception as e:
                    traceback.print_exc(e)
                if name == "级  别":
                    level = value
                elif name == "车身结构":
                    structure = value
                elif name == "发 动 机":
                    engine = value
                elif name == "变 速 箱":
                    transmission = value
                elif name == "充电时间":
                    chargingTime = value
                elif name == "续航里程":
                    mileage = value
                elif name == "电 动 机":
                    motor = value
                elif name == "外观颜色":
                    aList = li.find('div', class_='carcolor fn-left').find_all('a')
                    wcolor = ""
                    for a in aList:
                        try:
                            style = a.find('em')["style"][11:-1]
                            color = a.find('div', class_="tip-content").get_text()
                            wcolor = wcolor + color + "(" + style + ")" + ","
                        except Exception as e:
                            traceback.print_exc(e)
                    if len(wcolor) > 1:
                        wcolor = wcolor[0:-1]
            imgName, imgPath = self.download(imgUrl)
            sql = "INSERT INTO car_info (model_name, level, structure, price,motor, engine, transmission, charging_time, advance_price, mileage, rating, img_url, img_path, img_name, wcolor,brand_name,sell_status, class_name, initials_name) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cur = self.conn.cursor()
            cur.execute(sql, (
            modelName, level, structure, price, motor, engine, transmission, chargingTime, advancePrice,
            mileage, rating, imgUrl, imgPath, imgName, wcolor, brandName,sellStatus, item["className"],
            item["initialsName"]))
            self.conn.commit()

        return links

    def download(self, link):
        filename = str(self.myTotal)+re.findall(r'.*/(.+)', link)[0]
        try:
            pic = requests.get(link)
            imgPath="d:\\carimg" + os.sep +filename
            if pic.status_code == 200:
                with open(imgPath, 'wb') as fp:
                    fp.write(pic.content)
                    fp.close()
            return filename,imgPath
        except Exception as e:
            print(e)
            print("保存失败>>"+filename)