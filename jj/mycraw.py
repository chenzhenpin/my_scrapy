from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import requests
import json
import pymysql
count=1
conn = pymysql.connect(host="127.0.0.1", user="root", passwd="333333", db="yiche", charset="utf8")
def start(g,pageNum):
    MANUFACTURER=None
    if g==1:
        MANUFACTURER="01"
    elif g==2:
        MANUFACTURER = "02"
    elif g==4:
        MANUFACTURER = "03"
    for num in range(1,pageNum):
        r = requests.get("http://select.car.yiche.com/selectcartool/searchresult?g="+str(g)+"&page="+str(num)+"&external=Car&v=20171011&callback=jsonpCallback")
        pattern = re.compile(r"jsonpCallback\((.*)\)", re.MULTILINE | re.DOTALL)
        jsonstr=pattern.search(r.text).group(1)
        jsonObject=json.loads(jsonstr)
        ResList=jsonObject["ResList"]
        for model in ResList:
            sql='UPDATE car_model SET MANUFACTURER="'+MANUFACTURER+'" WHERE MODEL_NAME="'+model["ShowName"]+'"'
            print(sql)
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            global count
            count=count+1
    print(count)
if __name__ == '__main__':
    start(1,38)
    start(2,15)
    start(4,15)
