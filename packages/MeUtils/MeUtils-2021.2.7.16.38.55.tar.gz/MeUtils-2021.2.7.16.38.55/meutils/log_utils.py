#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : log_utils
# @Time         : 2020/11/12 11:40 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import os
import sys
from random import uniform
from loguru import logger

# LOG CONF: 需提前配置在环境变量里
LOG_PATH = os.environ.get('LOG_PATH')
LOG_LEVEL = os.environ.get('LOG_LEVEL', "INFO")

# todo: https://blog.csdn.net/bailang_zhizun/article/details/107863671
# 1. 过滤
# 2. 默认配置、zk配置、文件配置、环境变量配置
if LOG_PATH:
    logger.add(
        LOG_PATH,
        rotation="100 MB",
        enqueue=True,  # 异步
        encoding="utf-8",
        backtrace=True,
        diagnose=True,
        level=LOG_LEVEL,
        # filter=
    )


# 日志采样输出：按时间 按条数
def logger4sample(log, bins=10):
    if uniform(0, bins) < 1:
        logger.info(log)


# todo: 起个服务配置通用logger
def logger4feishu(title='这是一个标题', text='这是一条log'):
    import requests
    from meutils.zk_utils import get_zk_config
    webhook = get_zk_config('/mipush/bot/webhooks')['logger']

    r = requests.post(webhook, json={'title': title, 'text': text})
    return r.json()


# todo:
#  add zk/es/mongo/hdfs logger
# logger = logger.patch(lambda r: r.update(name=__file__))
logger_patch = lambda name: logger.patch(lambda r: r.update(name=name))  # main模块: 等价于 __name__=__file__

if __name__ == '__main__':
    logger.info("xx")
    logger4feishu()
