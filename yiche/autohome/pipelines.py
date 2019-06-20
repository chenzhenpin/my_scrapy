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
            self.model_num=0
            self.year_num=0
        except Exception as e:
            print(r'error connect--------------------------------------------------')
            traceback.print_exc(e)

    def process_item(self, item, spider):
        link='http://car.bitauto.com' + item['modelUrl']
        r=requests.get(link)
        soup=BeautifulSoup(r.text)
        lis=soup.find('ul',class_='list list-justified').find_all('li')
        MODEL_IMG = self.download1(item["modelImgUrl"])
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
                            levelCode= MODEL_YEAR=MODEL_VEHICLE= powerType=gearboxType=ENGINE_DISPLACE= ENGINE_DISPLACE_SUFFIX=FUEL_TYPE_CODE=CAR_COLOUR=seatNum=effluentStandard=mileage= CAR_IMG=None
                            for j,rowData in enumerate(yearModel):
                                if j==0:
                                    MODEL_YEAR=rowData[7]+"款 "
                                    MODEL_VEHICLE=rowData[1]


                                    CAR_COLOUR=rowData[13]
                                    if rowData[12]=="客车":
                                        levelCode ="07"
                                    elif rowData[12]=="皮卡车":
                                        levelCode = "06"
                                    elif rowData[12]=="面包":
                                        levelCode = "05"
                                    elif rowData[12]=="跑车":
                                        levelCode = "04"
                                    elif rowData[12]=="全尺寸SUV":
                                        levelCode = "0306"
                                    elif rowData[12]=="大型SUV":
                                        levelCode = "0305"
                                    elif rowData[12]=="中大型SUV":
                                        levelCode = "0304"
                                    elif rowData[12]=="中型SUV":
                                        levelCode = "0303"
                                    elif rowData[12]=="紧凑型SUV":
                                        levelCode = "0302"
                                    elif rowData[12]=="小型SUV":
                                        levelCode = "0301"
                                    elif rowData[12]=="SUV":
                                        levelCode = "03"
                                    elif rowData[12]=="MPV":
                                        levelCode = "02"
                                    elif rowData[12]=="豪华车":
                                        levelCode = "0106"
                                    elif rowData[12]=="中大型车":
                                        levelCode = "0105"
                                    elif rowData[12]=="中型车":
                                        levelCode = "0104"
                                    elif rowData[12]=="紧凑型车":
                                        levelCode = "0103"
                                    elif rowData[12]=="小型车":
                                        levelCode = "0102"
                                    elif rowData[12]=="微型车":
                                        levelCode = "0101"
                                    elif rowData[12]=="轿车":
                                        levelCode = "01"
                                    elif rowData[12]=="大型MPV":
                                        levelCode = "0204"
                                    elif rowData[12]=="中型MPV":
                                        levelCode = "0203"
                                    elif rowData[12]=="紧凑型MPV":
                                        levelCode = "0202"
                                    elif rowData[12]=="小型MPV":
                                        levelCode = "0201"
                                    elif rowData[12]=="重型卡车":
                                        levelCode = "0803"
                                    elif rowData[12]=="中型卡车":
                                        levelCode = "0802"
                                    elif rowData[12]=="轻型卡车":
                                        levelCode = "0801"
                                    elif rowData[12]=="卡车":
                                        levelCode = "08"
                                    elif rowData[12]=="大型跑车":
                                        levelCode = "0403"
                                    elif rowData[12]=="中型跑车":
                                        levelCode = "0402"
                                    elif rowData[12]=="小型跑车":
                                        levelCode = "0401"
                                    elif rowData[12]=="大型客车":
                                        levelCode = "0702"
                                    elif rowData[12]=="轻型客车":
                                        levelCode = "0701"
                                    else:
                                        levelCode=rowData[12]

                                if j==1:

                                    ENGINE_DISPLACE = rowData[4]
                                    if "自然吸气" in rowData[5]:
                                        ENGINE_DISPLACE_SUFFIX = "L"
                                    elif  "增压" in  rowData[5]:
                                        ENGINE_DISPLACE_SUFFIX = "T"
                                    else:
                                        ENGINE_DISPLACE_SUFFIX=rowData[5]

                                    if  rowData[14]=="汽油":
                                        powerType="01"
                                    elif rowData[14]=="柴油":
                                        powerType="02"
                                    elif "纯电" in rowData[14]:
                                        powerType="03"
                                    elif rowData[14]=="插电混合":
                                        powerType="04"
                                    elif rowData[14]=="油电混合":
                                        powerType="05"
                                    elif rowData[14]=="天然气":
                                        powerType="06"
                                    else:
                                        powerType=rowData[14]


                                    if rowData[8]=="手动":
                                        gearboxType='01'

                                    elif rowData[8]=="机械自动":
                                        gearboxType='02'

                                    elif rowData[8]=="自动":
                                        gearboxType='03'

                                    elif rowData[8]=="手自一体":
                                        gearboxType='04'

                                    elif rowData[8]=="CVT无级变速":
                                        gearboxType='05'

                                    elif rowData[8]=="E-CVT无级变速":
                                        gearboxType='06'

                                    elif rowData[8]=="单速变速箱":
                                        gearboxType='07'

                                    elif rowData[8]=="双离合":
                                        gearboxType='08'
                                    else:
                                        gearboxType=rowData[8]
                                if j==2:
                                    seatNum=rowData[5]
                                if j==3:
                                    if rowData[19]=="国六":
                                        effluentStandard='01'
                                    elif rowData[19]=="国五":
                                        effluentStandard='02'
                                    elif rowData[19]=="国四":
                                        effluentStandard='03'
                                    elif rowData[19]=="国三":
                                        effluentStandard='04'
                                    elif rowData[19]=="国二":
                                        effluentStandard='04'
                                    elif rowData[19]=="国一":
                                        effluentStandard='04'
                                    else:
                                        effluentStandard=rowData[19]

                                    if rowData[12]=="92号":
                                        FUEL_TYPE_CODE="01"
                                    elif rowData[12]=="95号":
                                        FUEL_TYPE_CODE = "02"
                                    elif rowData[12]=="98号":
                                        FUEL_TYPE_CODE = "03"
                                    elif rowData[12]=="柴油":
                                        FUEL_TYPE_CODE = "04"
                                    elif rowData[12]=="天然气":
                                        FUEL_TYPE_CODE = "05"
                                    else:
                                        FUEL_TYPE_CODE=rowData[12]
                                    mileage=rowData[30]

                            # sql = "INSERT INTO car_info (initials_name, brand_name, logo_url, logo_path, cadimg_url, carimg_path, model_name, level, car_name, power_type, gearbox_type, displacement, seat_num, effluent_standard, manufacturer, fuel_label, mileage) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                            # cur = self.conn.cursor()
                            # cur.execute(sql, (item["initialsName"],  item["brandName"], item["logoUrl"], '', item["modelImgUrl"], '', item["modelName"], level,carName,powerType, gearboxType, displacement, seatNum, effluentStandard,'', fuelLabel, mileage))
                            # self.conn.commit()
                            CAR_IMG=self.download2(yearModel[0][2])
                            sql = "INSERT INTO yiche.car_model (MODEL_NAME, FK_BRAND_ID, BRAND_NAME, LEVEL_CODE, MODEL_YEAR, MODEL_VEHICLE, ENGINE_TYPE, GEAR_BOX, ENGINE_DISPLACE, ENGINE_DISPLACE_SUFFIX, FUEL_TYPE_CODE, FK_ATTACH_ID, CAR_COLOUR, SEATS, DISCHARGE_STANDARD, MILEAGE, MANUFACTURER, MODEL_IMG, CAR_IMG, PRE_ATTR10) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                            cur = self.conn.cursor()
                            cur.execute(sql, (
                                item["modelName"], item["brandCode"],  item["brandName"], levelCode, MODEL_YEAR, MODEL_VEHICLE, powerType,
                                gearboxType, ENGINE_DISPLACE, ENGINE_DISPLACE_SUFFIX, FUEL_TYPE_CODE, None,
                                CAR_COLOUR, seatNum, effluentStandard, mileage, None, MODEL_IMG, CAR_IMG,
                                None))
                            self.conn.commit()


                # for li in lis:
                #     cartext=li.find('div',id='draggcarbox_1').find('dd').get_text()


        return item




    def download1(self, link):
        self.model_num=self.model_num+1
        filename = str(self.model_num)+re.findall(r'.*/(.+)', link)[0]
        try:
            pic = requests.get(link)
            imgPath="D:\carinfo\modelimg" + os.sep +filename
            if pic.status_code == 200:
                with open(imgPath, 'wb') as fp:
                    fp.write(pic.content)
                    fp.close()
            return "/uploads/carinfo/modelimg/"+filename
        except Exception as e:
            print(e)
            print("保存失败>>"+filename)
    def download2(self, link):
        self.year_num = self.year_num + 1
        filename = str(self.year_num)+re.findall(r'.*/(.+)', link)[0]
        try:
            pic = requests.get(link)
            imgPath="D:\carinfo\yearimg" + os.sep +filename
            if pic.status_code == 200:
                with open(imgPath, 'wb') as fp:
                    fp.write(pic.content)
                    fp.close()
            return "/uploads/carinfo/yearimg/"+filename
        except Exception as e:
            print(e)
            print("保存失败>>"+filename)