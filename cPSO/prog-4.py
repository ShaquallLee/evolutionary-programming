#!/usr/bin/env python
# encoding: utf-8
# @author: lishaogang
# @file: prog-4.py
# @time: 2020/6/28 0028 16:02
# @desc:
from config import test_funcs
from test3.GPSO import GPSO
from test3.LPSO import LPSO
import matplotlib.pyplot as plt
import math

dim = 100#30
size = 100#50
iter_num = 3000
x_max = 100
max_vel = 0.2
K = 4
# func_id = 0

for func_id in range(13):
    print("\n第{}个测试函数：".format(func_id))
    fig = plt.figure()

    gpso = GPSO(dim, size, iter_num, x_max, max_vel, W=1/(2*math.log10(2.0)),C1=0.5+math.log10(2.0),C2=0.5+math.log10(2.0), fit_func=test_funcs[func_id])
    fit_var_list, _ = gpso.update()
    print("gpso最优解:" + str(fit_var_list[-1]))
    ax = fig.add_subplot(221)
    ax.plot(fit_var_list)
    pso = LPSO(dim, size, iter_num, x_max, max_vel, W=1/(2*math.log10(2.0)),C1=0.5+math.log10(2.0),C2=0.5+math.log10(2.0),K=K)
    fit_var_list, _ = pso.update()
    print("lpso最优解:" + str(fit_var_list[-1]))
    ax = fig.add_subplot(222)
    ax.plot(fit_var_list)
    plt.show()