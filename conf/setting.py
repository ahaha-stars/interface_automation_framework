import os
import sys
import logging

#项目基础路径
DIR_BASE = os.path.dirname(os.path.dirname(__file__))
# print(DIR_BASE)

#log日志的输出级别
LOG_LEVEL = logging.DEBUG # 日志输出文件的级别
STREAM_LOG_LEVEL = logging.DEBUG  # 输出日志控制台

# 各个需要用到的文件的基础路径
FILE_PATH = {
    'extract' : os.path.join(DIR_BASE,'extract.yaml'),
    'conf': os.path.join(DIR_BASE,'conf','config.ini'),
    'LOG': os.path.join(DIR_BASE, 'logs')
}

print(FILE_PATH['extract'])
print(FILE_PATH['conf'])