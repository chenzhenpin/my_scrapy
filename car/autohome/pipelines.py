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
            self.conn = pymysql.connect(host="127.0.0.1", user="root", passwd="333333", db="car", charset="utf8")
            self.myTotal=0
            self.startTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(r'error connect--------------------------------------------------')
            traceback.print_exc(e)

    def process_item(self, item, spider):
        link='https://car.autohome.com.cn' + item['brandUrl']
        r = requests.get(link)
        soup = BeautifulSoup(r.text)
        brandImgUrl=soup.find('div',class_='uibox-con contbox').find('div',class_='carbradn-pic').img["src"]
        carTreeSrc=soup.find('div',id="cartree").script["src"]
        carTreeText = requests.get('https://car.autohome.com.cn'+carTreeSrc).text[18:-3]
        carTreeElem = BeautifulSoup(carTreeText)
        ddElems=carTreeElem.find('li',id=item['brandId']).find_all('dd')
        for ddElem in ddElems:
            modelText=ddElem.get_text()
            modelName=modelText[0:modelText.find("(")]
            modelLink=ddElem.a['href']
            yearModelLinkList=[]
            for yearModelLink in self.crawYearModelList(item,modelLink,yearModelLinkList,True):
                self.crawYearModelInfo(item,yearModelLink)
        return item


    def crawYearModelList(self,item,link,yearModelLinkList,flag):
        link = 'https://car.autohome.com.cn' + link
        r = requests.get(link)
        soup=BeautifulSoup(r.text)
        ulElems=soup.find_all('ul',class_='interval01-list')
        for ulElem in ulElems:
            liElems=ulElem.find_all('li')
            for liElem in liElems:
                yearModelLink=liElem.find('div', class_='interval01-list-cars-infor').find('p',id=re.compile("p*")).a['href']
                yearModelLinkList.append(yearModelLink)
        if flag==True:
            liClickElems = soup.find('div',class_='tab-nav border-t-no').find('ul', attrs={"data-trigger":"click"}).find_all('li')
            otherMoldeLinkList=[]
            for liClickElem in liClickElems:
                try:
                    if liClickElem['class']==['current'] or liClickElem['class']==['disabled']:
                        continue
                except Exception as e:
                    pass
                otherMoldeLinkList.append(liClickElem.a['href'])
            for otherMoldeLink in otherMoldeLinkList:
                self.crawYearModelList(item,otherMoldeLink,yearModelLinkList,False)
        return yearModelLinkList
    def crawYearModelInfo(self,item,yearModelList):
        r = requests.get("https:"+yearModelList)
        soup = BeautifulSoup(r.text)
        return item
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