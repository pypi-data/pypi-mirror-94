#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : crontab
# @Time         : 2021/2/7 5:33 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.zk_utils import get_zk_config


class Cron(object):
    """doc"""

    def __init__(self, **kwargs):
        pass

    def add(self, command, comment):
        with CronTab(True) as cron:
            logger.warning(f"ADD cron: {command}")
            cron.new(command, comment, pre_comment=True)

    def remove(self):
        pass

    def update_from_file(self, path='/mipush/crontab/mitv'):
        """从zk同步cron: 可配置每天第一分钟同步crontab配置信息（zk/yaml） 1 0 * * *


        :param path: zk/yaml
            comment1:
              - cmd1
              - cmd2
        :return:
        """
        crontabs = yaml_load(path) if Path('path').isfile() else get_zk_config(path)
        logger.info(f"Crontab update to: {bjson(crontabs)}")

        with CronTab(True) as cron:
            for comment, cmds in crontabs.items():
                # 删除
                jobs = cron.find_comment(comment)
                for job in jobs:
                    cron.remove(job)

                # 新增
                for cmd in cmds:
                    cron.new(cmd, comment, pre_comment=True)


def main():
    fire.Fire(Cron)


if __name__ == '__main__':
    Cron()
