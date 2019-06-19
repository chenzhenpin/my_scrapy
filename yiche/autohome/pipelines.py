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
import json
import random
class AutohomePipeline(object):
    def __init__(self):
        try:
            self.conn = pymysql.connect(host="127.0.0.1", user="root", passwd="333333", db="yiche", charset="utf8")
            self.myTotal=0
        except Exception as e:
            print(r'error connect--------------------------------------------------')
            traceback.print_exc(e)

    def process_item(self, item, spider):
        link='http://car.bitauto.com' + item['modelUrl']
        r=requests.get(link)
        soup=BeautifulSoup(r.text)
        lis=soup.find('ul',class_='list list-justified').find_all('li')
        for li in lis:
            if li.get_text()=='参数配置':
                href="http://car.bitauto.com"+li.a['href']
                b=requests.get(href)
                conf = BeautifulSoup(b.text)
                scripts=conf.find_all('script')
                for script in scripts:
                    if "carCompareJson" in script.text:
                        jsonData=json.loads(script.text[script.text.find('['):script.text.find('];')+1])
                        print(jsonData)
                        for i,yearModel in enumerate(jsonData):
                            carName=level=powerType=gearboxType=seatNum=displacement=effluentStandard=fuelLabel=mileage=None;
                            for j,rowData in enumerate(yearModel):
                                if j==0:
                                    carName=rowData[7]+"款 "+rowData[1]
                                    level=rowData[12]
                                    displacement = rowData[1][0:3]
                                if j==1:

                                    powerType=rowData[14]
                                    gearboxType=rowData[8]
                                if j==2:
                                    seatNum=rowData[5]
                                if j==3:
                                    effluentStandard=rowData[19]
                                    fuelLabel=rowData[12]
                                    mileage=rowData[30]

                            sql = "INSERT INTO car_info (initials_name, brand_name, logo_url, logo_path, cadimg_url, carimg_path, model_name, level, car_name, power_type, gearbox_type, displacement, seat_num, effluent_standard, manufacturer, fuel_label, mileage) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                            cur = self.conn.cursor()
                            cur.execute(sql, (item["initialsName"],  item["brandName"], item["logoUrl"], '', item["modelImgUrl"], '', item["modelName"], level,carName,powerType, gearboxType, displacement, seatNum, effluentStandard,'', fuelLabel, mileage))
                            self.conn.commit()

                # for li in lis:
                #     cartext=li.find('div',id='draggcarbox_1').find('dd').get_text()


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