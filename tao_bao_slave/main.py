from scrapy.cmdline import execute
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(['scrapy', 'crawl', 'taobao_slave'])  # 你需要将此处的spider_name替换为你自己的爬虫名称