#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : DeepNN.
# @File         : decorator_utils
# @Time         : 2020/4/30 10:46 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


class Singleton:
    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.cls(*args, **kwargs)
        return self.instance


if __name__ == '__main__':
    import time


    class A:

        def __init__(self, ):
            print('A实例化')


    @Singleton
    class B:
        def __init__(self, ):
            print('B实例化')


    for _ in range(3):
        print('\n', _)
        A()
        B()
