#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : common
# @Time         : 2021/2/7 4:42 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *

import typer

cli = typer.Typer(name="MeUtils CLI")


@cli.command
def cron(action='add', command=None, comment=None):
    with CronTab(True) as cron:
        # crons = cron | xlist  # cron.crons
        # cron_commands = cron.commands | xlist
        # cron_comments = cron.comments | xlist

        # add
        if action == 'add':
            cron.new(command=command, comment=comment, pre_comment=True)


if __name__ == '__main__':
    cli()
