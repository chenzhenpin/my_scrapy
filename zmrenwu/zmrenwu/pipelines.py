# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from datetime import datetime
class ZmrenwuPipeline(object):

    def __init__(self):
        try:
            print('======================================================================================')
            self.conn=pymysql.connect(host="127.0.0.1",user="chenzhen",passwd="123456",db="my_django",charset="utf8")

        except:
            print(r'error connect--------------------------------------------------')
    def process_item(self, item, spider):
        #from_url=item['from_url']
        body=''
        for i in item['content']:
            body=i
        title=item['title']

        created_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        modified_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 文章摘要，可以没有文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错。
        # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
        excerpt = ''


        category_id = 1
        views = 0

        # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
        # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
        # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
        # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
        author_id = 1


        sql = "insert into app_blog_post(title,body,created_time,modified_time,excerpt,category_id,views,author_id)  VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        cur = self.conn.cursor()
        cur.execute(sql, (title,body,created_time,modified_time,excerpt,category_id,views,author_id))
        self.conn.commit()

        return item

    def close_spider(self,spider):
        self.conn.close()
