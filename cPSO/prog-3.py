#!/usr/bin/env python
# encoding: utf-8
# @author: lishaogang
# @file: prog-3.py
# @time: 2020/6/27 0027 9:44
# @desc: 局部版的粒子群优化

from test3.LPSO import LPSO
import matplotlib.pyplot as plt
import numpy as np
import math


dim = 100
size = 100
iter_num = 3000
x_max = 100
max_vel = 0.2

K = 4

pso = LPSO(dim, size, iter_num, x_max, max_vel, W=1/(2*math.log10(2.0)),C1=0.5+math.log10(2.0),C2=0.5+math.log10(2.0),K=K)
fit_var_list, best_pos = pso.update()
print("最优位置:" + str(best_pos))
print("最优解:" + str(fit_var_list[-1]))
plt.plot(np.linspace(0, iter_num, iter_num), fit_var_list)
plt.show()

