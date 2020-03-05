# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from tao_bao_slave.items import TaoBaoSlaveItem
from tao_bao_slave.login_taobao import UsernameLogin, COOKIES_FILE_PATH
from tao_bao_slave.settings import USER_AGENT_LIST, PROXY_POOL_URL
import time
import json
import requests
import random
import re
import redis

class TaobaoSlaveSpider(RedisSpider):
    name = 'taobao_slave'
    allowed_domains = ['s.taobao.com']
    #start_urls = ['http://www.taobao.com/']
    redis_key = 'tao_bao:requests'
    db = redis.StrictRedis(host='10.10.10.104', port='6379', password='77cc77',decode_responses=True)
    Login = UsernameLogin()
    Login.login()
    with open(Login.username+COOKIES_FILE_PATH, 'r', encoding='utf-8') as file:
        cookies = json.load(file)

    #重写make_requests_from_url添加cookies
    def make_requests_from_url(self, url):
        print(url)
        return Request(url, cookies=self.cookies)

    def response_retry(self, response):  #用于出现滑块重试
        request = response.request.replace(url=response.meta.get('original_request_url', response.url))
        request.dont_filter = True  # 重试的URL不会被过滤


    def parse(self, response):
        if response:
            # print('ip=',response.text)
            #print(response.text)
            products_str = re.search(r'g_page_config = (.*?)}};', response.text)
            try:
                products_str = products_str.group(1) + '}}'
            except:
                print('出现滑块')
                self.db.lpush('tao_bao:resquests', response.url)
                yield self.response_retry(response)
            products_json = json.loads(products_str)
            products_list = products_json['mods']['itemlist']['data']['auctions']
            for products in products_list:
                item = TaoBaoSlaveItem()
                item['trade_name'] = products['raw_title']
                item['sales_volume'] = products['view_sales']
                item['price'] = products['view_price']
                item['address'] = products['item_loc']
                item['trade_url'] = products['detail_url'][2:]
                yield item