#!/usr/bin/env python
# encoding: utf-8
# @author: lishaogang
# @file: Particle.py
# @time: 2020/7/5 0005 9:30
# @desc:

import random

class Particle():
    def __init__(self, MAXDIM, lbound, rbound, F, CR, calc_fitness):
        self.gene = [lbound+random.random()*(rbound-lbound) for i in range(MAXDIM)]
        self.fitness = calc_fitness(self.gene)
        self.F = F
        self.CR = CR
        self.paretorank = 0    # 拥挤等级
        self.ndd = 0 # 拥挤距离

if __name__ == '__main__':
    pass
