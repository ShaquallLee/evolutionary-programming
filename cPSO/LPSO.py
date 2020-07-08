#!/usr/bin/env python
# encoding: utf-8
# @author: lishaogang
# @file: LPSO.py
# @time: 2020/6/27 0027 9:36
# @desc: 局部粒子群最优优化

import numpy as np
import random


def fit_fun(X):  # 适应函数
    sum = 0
    for x in X:
        sum += x**2
    return sum

def random_nums(lbound, ubound, forbiden_i, K):
    '''
    随机k个不同的数
    :param lbound:
    :param ubound:
    :param forbiden_i:
    :param K:
    :return:
    '''
    nei = []
    i = 0
    while i < K:
        n = random.randint(lbound, ubound)
        if n not in nei and n != forbiden_i:
            nei.append(n)
            i += 1
    return nei

class Particle:
    # 初始化
    def __init__(self, x_max, max_vel, dim, K, swarm_size, forbiden_i):
        self.__pos = [random.uniform(-x_max, x_max) for i in range(dim)]  # 粒子的位置
        self.__vel = [random.uniform(-max_vel, max_vel) for i in range(dim)]  # 粒子的速度
        self.__bestPos = [0.0 for i in range(dim)]  # 粒子最好的位置
        self.__fitnessValue = fit_fun(self.__pos)  # 适应度函数值
        self.neighbors = random_nums(0, swarm_size-1, forbiden_i, K)   #K个近邻
        self.lBest = self   # 局部最优

    def set_pos(self, i, value):
        self.__pos[i] = value

    def get_pos(self):
        return self.__pos

    def set_best_pos(self, i, value):
        self.__bestPos[i] = value

    def get_best_pos(self):
        return self.__bestPos

    def set_vel(self, i, value):
        self.__vel[i] = value

    def get_vel(self):
        return self.__vel

    def set_fitness_value(self, value):
        self.__fitnessValue = value

    def get_fitness_value(self):
        return self.__fitnessValue


class LPSO:
    def __init__(self, dim, size, iter_num, x_max, max_vel, C1, C2, W, K, best_fitness_value=float('Inf')):
        self.C1 = C1
        self.C2 = C2
        self.W = W
        self.K = K  # 邻居个数
        self.is_update = False # 全局最优是否有更新
        self.dim = dim  # 粒子的维度
        self.size = size  # 粒子个数
        self.iter_num = iter_num  # 迭代次数
        self.x_max = x_max      #取值域最大值
        self.max_vel = max_vel  # 粒子最大速度
        self.best_fitness_value = best_fitness_value    #最优适应值
        self.best_position = [0.0 for i in range(dim)]  # 种群最优位置
        self.fitness_val_list = []  # 每次迭代最优适应值

        # 对种群进行初始化
        self.Particle_list = [Particle(self.x_max, self.max_vel, self.dim, self.K, self.size, i) for i in range(self.size)]

    def set_bestFitnessValue(self, value):
        self.best_fitness_value = value

    def get_bestFitnessValue(self):
        return self.best_fitness_value

    def set_bestPosition(self, i, value):
        self.best_position[i] = value

    def get_bestPosition(self):
        return self.best_position

    # 找到局部最优
    def update_lbest(self,part):
        for j in range(self.K):
            if part.lBest.get_fitness_value() > self.Particle_list[part.neighbors[j]].get_fitness_value():
                part.lBest = self.Particle_list[part.neighbors[j]]

    # 更新速度
    def update_vel(self, part):
        for i in range(self.dim):
            vel_value = self.W * part.get_vel()[i] + self.C1 * random.random() * (part.get_best_pos()[i] - part.get_pos()[i]) \
                        + self.C2 * random.random() * (self.get_bestPosition()[i] - part.get_pos()[i])
            if vel_value > self.max_vel:
                vel_value = self.max_vel
            elif vel_value < -self.max_vel:
                vel_value = -self.max_vel
            part.set_vel(i, vel_value)

    # 更新位置
    def update_pos(self, part):
        for i in range(self.dim):
            pos_value = part.get_pos()[i] + part.get_vel()[i]
            if pos_value < -self.x_max:
                pos_value = 2 * (-self.x_max) - pos_value
                part.set_vel(i, -part.get_vel()[i])
            if pos_value > self.x_max:
                pos_value = 2* self.x_max - pos_value
                part.set_vel(i, -part.get_vel()[i])
            part.set_pos(i, pos_value)

        value = fit_fun(part.get_pos())
        if value < part.get_fitness_value():
            part.set_fitness_value(value)
            for i in range(self.dim):
                part.set_best_pos(i, part.get_pos()[i])
        if value < self.get_bestFitnessValue():
            self.set_bestFitnessValue(value)
            self.is_update = True
            for i in range(self.dim):
                self.set_bestPosition(i, part.get_pos()[i])

    def update(self):
        for i in range(self.iter_num):
            self.is_update = False
            for part in self.Particle_list:
                self.update_lbest(part) # 更新局部最优
                self.update_vel(part)  # 更新速度
                self.update_pos(part)  # 更新位置
            self.fitness_val_list.append(self.get_bestFitnessValue())  # 每次迭代完把当前的最优适应度存到列表
            if not self.is_update:
                for i in range(self.size):
                    self.Particle_list[i].neighbors = random_nums(0, self.size-1,i,self.K)
        return self.fitness_val_list, self.get_bestPosition()