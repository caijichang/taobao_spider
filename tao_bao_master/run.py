#from ProxyPool.proxypool.scheduler import Scheduler
from scheduler import Scheduler
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    try:
        s = Scheduler()
        s.run()
    except:
        main()


if __name__ == '__main__':
    main()
    print('ip池地址：http://0.0.0.0:5555/random')