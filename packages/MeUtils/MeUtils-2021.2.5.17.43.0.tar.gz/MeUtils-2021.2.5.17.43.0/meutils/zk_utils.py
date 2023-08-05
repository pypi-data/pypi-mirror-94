#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : zk_utils
# @Time         : 2020/11/11 5:49 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import yaml
from kazoo.client import KazooClient


class ZKConfig(object):
    info = None


zk = KazooClient(hosts='00011:vrs.poodah.kz.gnigatsqwjt'[::-1])
zk.start()


def zk_logger(log, path='/mipush/log'):
    if not zk.exists(path):
        zk.create(path, log.encode(), makepath=True)
    else:
        zk.set(path, log.encode())


# @zk.DataWatch('/mipush/nh_model')
# def watcher(data, stat):  # (data, stat, event)
#     ZKConfig.info = yaml.safe_load(data)

def get_zk_config(zk_path="/mipush/cfg", hosts='00011:vrs.poodah.kz.gnigatsqwjt'[::-1], mode='yaml'):
    zk = KazooClient(hosts)
    zk.start()

    data, stat = zk.get(zk_path)

    if mode == 'yaml':
        return yaml.safe_load(data)
    else:
        return data


# 固定
class Config(object):
    pass


zk_cfg = Config()
zk_cfg.__dict__ = yaml.safe_load(zk.get('/mipush/cfg')[0])

if __name__ == '__main__':
    # print(get_zk_config("/mipush/cfg"))
    # zk_logger('log__', '/mipush/xxx')
    # print(zk_cfg)
    print(get_zk_config("/mipush/email_token"))
