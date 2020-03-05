import time
from multiprocessing import Process
from ProxyPool.proxypool.api import app
from ProxyPool.proxypool.getter import Getter
from ProxyPool.proxypool.tester import Tester
from ProxyPool.proxypool.db import RedisClient
from ProxyPool.proxypool.setting import *
from ProxyPool.proxypool.proxypool_log import print_messege
from settings import REDIS_HOST,REDIS_PORT,REDIS_PASSWORD,GOODS_NAME,MAX_PAGE
import redis


class Scheduler():
    def __init__(self):
        self.db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)
        if 'tao_bao:requests' in self.db.keys():
            self.db.delete('tao_bao:requests')

    def schedule_tester(self, cycle=TESTER_CYCLE):
        """
        定时测试代理
        """
        tester = Tester()
        while True:
            print_messege('测试器开始运行')
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取代理
        """
        getter = Getter()
        while True:
            print_messege('开始抓取代理')
            getter.run()
            time.sleep(cycle)


    def schedule_api(self):
        """
        开启API
        """
        app.run(API_HOST, API_PORT)

    def schedule_insert_url(self):
        len = 0
        print(1)
        while True:
            if 'tao_bao:requests' not in self.db.keys() and len+10<=MAX_PAGE:
                len = len +10
                for page in range(len-10,len):
                    url = 'https://s.taobao.com/search?q=' + GOODS_NAME + '&s=' + str(page*44)
                    self.db.lpush('tao_bao:requests', url)
            time.sleep(10)

    def run(self):
        print_messege('代理池开始运行')

        insert_url_process = Process(target=self.schedule_insert_url)
        insert_url_process.start()

        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()



