#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : best_table
# @Time         : 2021/1/28 8:17 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *

df = pd.DataFrame(np.random.random((10, 10)))
tb = Besttable.dfdraw(df)
print(tb)
