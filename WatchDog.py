import configparser
import os
import time
from logging import handlers
from threading import Thread

import pyclamd
from watchdog.events import *
from watchdog.observers import Observer

logger = logging.getLogger('watch.log')
format_str = logging.Formatter('%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')  # 设置日志格式
logger.setLevel(logging.DEBUG)  # 设置日志级别
sh = logging.StreamHandler()  # 往屏幕上输出
sh.setFormatter(format_str)  # 设置屏幕上显示的格式
th = handlers.TimedRotatingFileHandler(filename='watch.log', when='D', backupCount=3,
                                       encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
# 实例化TimedRotatingFileHandler
# interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
# S 秒
# M 分
# H 小时、
# D 天、
# W 每星期（interval==0时代表星期一）
# midnight 每天凌晨
th.setFormatter(format_str)  # 设置文件里写入的格式
logger.addHandler(sh)  # 把对象加到logger里
logger.addHandler(th)






class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        logger.info("文件被修改了 %s" % event.src_path)
        file = event.src_path
        if os.path.isfile(file):
            os(file)

    def on_created(self, event):
        logger.info("文件被创建了 %s" % event.src_path)
        file = event.src_path
        if os.path.isfile(file):
            scan01(file)


if __name__ == "__main__":

    root_dir = os.path.abspath('.')  # 获取当前文件所在目录的上一级目录，即项目所在目录E:\Crawler
    cf = configparser.ConfigParser()
    cf.read(root_dir + "\config.ini")  # 拼接得到config.ini文件的路径，直接使用
    secs = cf.sections()  # 获取文件中所有的section(一个配置文件中可以有多个配置，如数据库相关的配置，邮箱相关的配置，
    watch_path = cf.get("FileSection", "watch-path")  # 获取[Mysql-Database]中host对应的值

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, watch_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()
    observer.join()
