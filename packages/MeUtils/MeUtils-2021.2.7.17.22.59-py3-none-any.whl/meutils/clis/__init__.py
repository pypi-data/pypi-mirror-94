#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : __init__.py
# @Time         : 2021/1/31 10:20 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from meutils.zk_utils import get_zk_config

import typer

cli = typer.Typer(name="MeUtils CLI")


@cli.command()
def hello(name: str):
    typer.echo(f"Hello {name}")


@cli.command()
def zk2crontab(zk_path='/mipush/crontab/mitv'):  # todo: yaml
    """从zk同步cron"""
    zk_crons = get_zk_config(zk_path)
    print(Besttable.draw_dict(zk_crons))

    with CronTab(True) as cron:
        for comment, cmds in zk_crons.items():
            # 删除
            jobs = cron.find_comment(comment)
            for job in jobs:
                cron.remove(job)

            # 新增
            for cmd in cmds:
                cron.new(cmd, comment, pre_comment=True)


@cli.command()
def crontab(command, comment, action='add'):
    with CronTab(True) as cron:
        # crons = cron | xlist  # cron.crons
        # cron_commands = cron.commands | xlist
        # cron_comments = cron.comments | xlist

        # add
        if action == 'add':
            logger.warning(f"CronTab: {command}")
            cron.new(command=command, comment=comment, pre_comment=True)


if __name__ == '__main__':
    cli()
