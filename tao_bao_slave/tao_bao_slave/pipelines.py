# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from tao_bao_slave.settings import MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT

class TaoBaoSlavePipeline(object):
    def __init__(self):
        self.db = pymysql.connect(host=MYSQL_HOST, user='root', passwd=MYSQL_PASSWORD,db='GOODS', charset='utf8',port=MYSQL_PORT)
        self.cur = self.db.cursor()

    def process_item(self, item, spider):
        sql = '''INSERT INTO GOODS(trade_name,price,sales_volume,address,trade_url) VALUES(%s,%s,%s,%s,%s) '''
        self.cur.execute(sql, (pymysql.escape_string(item['trade_name']), pymysql.escape_string(item['price']), pymysql.escape_string(item['sales_volume']), pymysql.escape_string(item['address']), pymysql.escape_string(item['trade_url'])))
        self.db.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.db.close()
