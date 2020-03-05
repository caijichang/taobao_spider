import logging
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s "#配置输出日志格式
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S  ' #配置输出时间的格式，注意月份和天数不要搞乱了
logging.basicConfig(level=logging.INFO,
                    format=LOG_FORMAT,
                    datefmt = DATE_FORMAT ,
                    filename="proxypool.log",   #有了filename参数就不会直接输出显示到控制台，而是直接写入文件
                    filemode='w'        #w为覆盖，a为不覆盖
                    )

def print_messege(*messege):
    logging.info(messege)

def warm_messege(*messege):
    logging.warning(messege)

def error_messege(*messege):
    logging.error(messege)