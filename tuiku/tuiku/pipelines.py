# coding=utf-8
# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from datetime import datetime
import urllib.request
import http.cookiejar
from bs4 import BeautifulSoup
import re
import sys,io
class TuikuPipeline(object):

    def __init__(self):
        try:
            self.conn=pymysql.connect(host="127.0.0.1",user="chenzhen",passwd="123456",db="flask",charset="utf8")

        except:
            print(r'error connect--------------------------------------------------')

    def process_item(self, item, spider):
        headers = {

            "Host": "www.tuicool.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:47.0) Gecko/20100101 Firefox/47.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Referer": "http://www.tuicool.com/ah",
            "Cookie": "_tuicool_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFRkkiJTM3OTJjMjMyMDhhMjJlMWE4YWI2MzM0MDZmM2M0YzZjBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMTNNbzhNa2FPdGsxZ0lIdmRzdFhyYW1BbWFWeVNaNmlMOXpiMTgzdWtUcG89BjsARg%3D%3D--3cf27db1a9f4a8a445fd1affd21be2c766ee4e43; UM_distinctid=15d764b8f6b9-00814053c058b6-395d7a1b-100200-15d764b8f6cf5; CNZZDATA5541078=cnzz_eid%3D2029289137-1500925610-%26ntime%3D1500925610; Hm_lvt_3c8ecbfa472e76b0340d7a701a04197e=1500928256; Hm_lpvt_3c8ecbfa472e76b0340d7a701a04197e=1500930745",
            "Connection": "keep-alive",
            "If-None-Match": 'W/"5beeb71dbd8827790ae2c796ea1cb594"',
            "Cache-Control": "max-age=0"

        }
        for j in range(0,len(item['title'])):
            tuiku_url = "http://www.tuicool.com"+item['tuiku_url'][j]

            cjar=http.cookiejar.CookieJar()
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
            headall=[]
            for k,v in headers.items():
                it=(k,v)
                headall.append(it)
            opener.addheaders=headall
            urllib.request.install_opener(opener)
            data=urllib.request.urlopen(tuiku_url).read().decode('utf-8')
            soup=BeautifulSoup(data)
            form_url = ''
            url=soup.find_all('a', class_="cut cut70")
            for i in url:
                form_url=i.get_text()

            title = item['title'][j] or ''

            content=''
            c=soup.find_all('div', class_="article_body")
            for i in c :
                content=str(i)
            #theme = item['theme'][j]
            theme = ""
            th= soup.find_all('span', class_="new-label")
            for i in th:
                theme=i.get_text()+';'+theme
            website = item['website'][j]
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            sql = "insert into tuiku(tuiku_url,form_url,title,content,theme,website,timestamp)  VALUES(%s,%s,%s,%s,%s,%s,%s)"
            cur=self.conn.cursor()
            cur.execute(sql,(tuiku_url,form_url,title,content,theme,website,timestamp))
            self.conn.commit()


    def close_spider(self,spider):
        self.conn.close()
