import redis
import time
from multiprocessing import Process
from settings import REDIS_HOST,REDIS_PORT,REDIS_PASSWORD,GOODS_NAME,MAX_PAGE,EMPTY_QUEUE

class start_url():

    def __init__(self):
        self.db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

        if 'tao_bao:requests' in self.db.keys() and EMPTY_QUEUE:
            self.db.delete('tao_bao:requests')

    def schedule_insert_url(self):
        len = 0
        while True:
            if 'tao_bao:requests' not in self.db.keys() and len+10<=MAX_PAGE:
                len = len +10
                for page in range(len-10,len):
                    url = 'https://s.taobao.com/search?q=' + GOODS_NAME + '&s=' + str(page*44)
                    self.db.lpush('tao_bao:requests', url)
            time.sleep(900)

    def run(self):
        insert_url = Process(target=self.schedule_insert_url())
        insert_url.start()


if __name__ == '__main__':
    pass