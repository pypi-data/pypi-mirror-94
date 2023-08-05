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

import typer

cli = typer.Typer(name="MeUtils CLI")


@cli.command()
def cron(command, comment, action='add'):
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
