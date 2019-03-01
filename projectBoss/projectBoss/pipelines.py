# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from redis import Redis


# 存入txt文档
class ProjectbossPipeline(object):

    f = None

    def open_spider(self, spider):
        self.f = open("boss.txt", "w", encoding="utf-8")

    # 爬虫文件每向管道提交一次item,则该方法就会被调用一次.
    # 参数:item 就是管道接收到的item类型对象
    def process_item(self, item, spider):
        self.f.write(item["job_name"] + "----" + item["salary"] + "----" + item["company"]  + "\n")
        # 返回给下一个即将被执行的管道类
        return item

    def close_spider(self, spider):
        self.f.close()


# 存入redis
class RedisbossPipeline(object):

    redis_obj = None

    def open_spider(self, spider):
        self.redis_obj = Redis(host="127.0.0.1", port=6379)

    # 爬虫文件每向管道提交一次item,则该方法就会被调用一次.
    # 参数:item 就是管道接收到的item类型对象
    def process_item(self, item, spider):
        dic = {
            'job_name': item['job_name'],
            'salary': item['salary'],
            'company': item['company']
        }
        self.redis_obj.lpush('boss', dic)
        # 返回给下一个即将被执行的管道类
        return item


class MysqlbossPipeline(object):

    mysql_obj = None
    cursor = None

    def open_spider(self, spider):
        self.mysql_obj = pymysql.Connect(host="127.0.0.1", port=3306, user="root", password="", db="db_boss", charset="utf8")

    # 爬虫文件每向管道提交一次item,则该方法就会被调用一次.
    # 参数:item 就是管道接收到的item类型对象
    def process_item(self, item, spider):
        self.cursor = self.mysql_obj.cursor()
        try:
            self.cursor.execute(
                'insert into boss values ("%s","%s","%s")' % (item['job_name'], item['salary'], item['company']))
            self.mysql_obj.commit()
        except Exception as e:
            print(e)
            self.mysql_obj.rollback()
        return item

    def close_spider(self, spider):
        self.mysql_obj.close()
        self.cursor.close()
