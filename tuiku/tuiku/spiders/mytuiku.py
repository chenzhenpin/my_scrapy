# -*- coding: utf-8 -*-
import scrapy
from tuiku.items import TuikuItem
from scrapy.http import Request

class MytuikuSpider(scrapy.Spider):
	name = "mytuiku"

	allowed_domains = ["tuicool.com"]
    
	def start_requests(self):
		print('start------------------------------')
		# yield  Request("http://127.0.0.1:5000")
		yield Request("http://www.tuicool.com/ah/0/1?lang=1",
					  headers={

							"Host": "www.tuicool.com",
							"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:47.0) Gecko/20100101 Firefox/47.0",
							"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
							"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
							"Accept-Encoding": "gzip, deflate",
							"Referer": "http://www.tuicool.com/ah",
							"Cookie": "_tuicool_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFRkkiJTM3OTJjMjMyMDhhMjJlMWE4YWI2MzM0MDZmM2M0YzZjBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMTNNbzhNa2FPdGsxZ0lIdmRzdFhyYW1BbWFWeVNaNmlMOXpiMTgzdWtUcG89BjsARg%3D%3D--3cf27db1a9f4a8a445fd1affd21be2c766ee4e43; UM_distinctid=15d764b8f6b9-00814053c058b6-395d7a1b-100200-15d764b8f6cf5; CNZZDATA5541078=cnzz_eid%3D2029289137-1500925610-%26ntime%3D1500925610; Hm_lvt_3c8ecbfa472e76b0340d7a701a04197e=1500928256; Hm_lpvt_3c8ecbfa472e76b0340d7a701a04197e=1500930745",
							"Connection": "keep-alive",
							"If-None-Match": 'W/"5beeb71dbd8827790ae2c796ea1cb594"',
							"Cache-Control": "max-age=0"

							  })


		# PR = Request(
		# 	'http://www.tuicool.com/ah',
		# 	headers=self.headers,
		# 	meta={'newrequest': Request(random_form_page, headers=self.headers)},
		# 	callback=self.parse_PR,
		# 	dont_filter=True
		# )
		# yield PR



	def parse(self, response):
		print('ok------------')
		item = TuikuItem()
		print(response)

		item["title"]=response.xpath("//div[@class='title']/a/@title").extract()

		item["tuiku_url"]=response.xpath("//div[@class='title']/a/@href").extract()
		item["website"]=response.xpath("//div[@class='tip']/span[1]/text()").extract()
		#返回数据到管道
		yield item

		for i in  range(2,60):
			url="http://www.tuicool.com/ah/0/"+str(i)+"?lang=1"
			print(url)
			yield Request(url,callback=self.parse,
						  headers={
							  "Host": "www.tuicool.com",
							  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:47.0) Gecko/20100101 Firefox/47.0",
							  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
							  "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
							  "Accept-Encoding": "gzip, deflate",
							  "Referer": "http://www.tuicool.com/ah",
							  "Cookie": "_tuicool_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFRkkiJTM3OTJjMjMyMDhhMjJlMWE4YWI2MzM0MDZmM2M0YzZjBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMTNNbzhNa2FPdGsxZ0lIdmRzdFhyYW1BbWFWeVNaNmlMOXpiMTgzdWtUcG89BjsARg%3D%3D--3cf27db1a9f4a8a445fd1affd21be2c766ee4e43; UM_distinctid=15d764b8f6b9-00814053c058b6-395d7a1b-100200-15d764b8f6cf5; CNZZDATA5541078=cnzz_eid%3D2029289137-1500925610-%26ntime%3D1500925610; Hm_lvt_3c8ecbfa472e76b0340d7a701a04197e=1500928256; Hm_lpvt_3c8ecbfa472e76b0340d7a701a04197e=1500930745",
							  "Connection": "keep-alive",
							  "If-None-Match": 'W/"5beeb71dbd8827790ae2c796ea1cb594"',
							  "Cache-Control": "max-age=0"
    				  })
		return item



