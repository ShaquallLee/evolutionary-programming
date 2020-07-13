#!/usr/bin/env python
# encoding: utf-8
# @author: lishaogang
# @file: Particle.py
# @time: 2020/7/5 0005 9:30
# @desc:

import random

class Particle():
    def __init__(self, MAXDIM, lbound, rbound, calc_fitness):
        self.gene = [lbound+random.random()*(rbound-lbound) for i in range(MAXDIM)]
        self.fitness = calc_fitness(self.gene)
        self.F = 0
        self.CR = 0
        self.old_F = random.random()
        self.old_CR =random.random()

if __name__ == '__main__':
    pass
