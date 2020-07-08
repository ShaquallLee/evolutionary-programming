#!/usr/bin/env python
# encoding: utf-8
# @author: lishaogang
# @file: test.py
# @time: 2020/6/25 0025 9:22
# @desc:

from test3.GPSO import GPSO
import matplotlib.pyplot as plt
import numpy as np
import math

from config import test_funcs

dim = 100#30
size = 100#50
iter_num = 3000
x_max = 100
max_vel = 0.2

func_id = 0

pso = GPSO(dim, size, iter_num, x_max, max_vel, W=1/(2*math.log10(2.0)),C1=0.5+math.log10(2.0),C2=0.5+math.log10(2.0), fit_func=test_funcs[func_id])
fit_var_list, best_pos = pso.update()
print("最优位置:" + str(best_pos))
print("最优解:" + str(fit_var_list[-1]))
plt.plot(np.linspace(0, iter_num, iter_num), fit_var_list)
plt.show()

