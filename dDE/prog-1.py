#!/usr/bin/env python
# encoding: utf-8
# @author: lishaogang
# @file: prog-1.py
# @time: 2020/7/5 0005 10:41
# @desc:
import matplotlib.pyplot as plt

from dDE.DE import DE
from config import test_funcs


MAXSIZE = 100
MAXDIM = 30
MAXGEN = 1500
TIMES = 1
# lbound = -1.28
# rbound = 1.28
func_id = 2
use_CD = False
use_NCD = True

# best = []
# with open('results/log.txt', 'w+') as log:
#     for func_id in range(len(test_funcs)):
for i in range(TIMES):
    de = DE(MAXSIZE, MAXDIM, MAXGEN, test_funcs[func_id]['func'],-test_funcs[func_id]['bound'],
            test_funcs[func_id]['bound'],use_CD=use_CD, use_NCD=use_NCD)
    de.update()
    print("the best fitness is ", de.bestFitnessValue)
    # log.write("func({})'s fitness：{}\n".format(func_id, de.bestFitnessValue))
    # best.append(de.bestFitnessValue)
    plt.plot(de.bestFitnessValues)
    plt.xlabel("generation\n\nfunc({})'s fitness".format(func_id))
    plt.ylabel('fitness')
    # plt.savefig("results/func{}.jpg".format(func_id))
    plt.show()


# the best fitness is  1.0579375764110492
# the best fitness is  596.6818781875263