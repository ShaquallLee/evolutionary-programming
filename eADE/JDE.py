#!/usr/bin/env python
# encoding: utf-8
# @author: lishaogang
# @file: DE.py
# @time: 2020/7/5 0005 9:29
# @desc:

from eADE.Particle import Particle
import random
import copy


class JDE():
    def __init__(self, MAXSIZE, MAXDIM, MAXGEN, calc_fitness, lbound, rbound, F=0.5, CR=0.9, use_CD=False, use_NCD=False):
        self.MAXSIZE = MAXSIZE
        self.MAXDIM = MAXDIM
        self.MAXGEN = MAXGEN
        self.lbound = lbound
        self.rbound = rbound
        self.tau1 = 0.1
        self.tau2 = 0.1
        self.Fl = 0.1
        self.Fu = 0.9
        self.calc_fitness = calc_fitness
        self.pop = [Particle(MAXDIM,lbound,rbound,F,CR, calc_fitness) for i in range(MAXSIZE)]    #初始种群
        self.donor_vector = [Particle(MAXDIM, lbound, rbound, F, CR, calc_fitness) for i in range(MAXSIZE)]
        self.bestFitnessValue = self.pop[0].fitness
        self.bestFitnessValues = []

    def update_bestfitness(self):
        best = self.pop[0]
        for i in range(1, self.MAXSIZE):
            if best.fitness > self.pop[i].fitness:
                best = self.pop[i]
        self.bestFitnessValue = best.fitness
        self.bestFitnessValues.append(best.fitness)

    def update(self):
        self.update_bestfitness()
        for i in range(self.MAXGEN):
            for j in range(self.MAXSIZE):
                self.mutation(j)
            for j in range(self.MAXSIZE):
                self.crossover(j)
            for j in range(self.MAXSIZE):
                self.select(j)
            self.bestFitnessValues.append(self.bestFitnessValue)


    def mutation(self, part_id):
        if random.random()<self.tau1:
            self.pop[part_id].F = self.Fl + random.random()*self.Fu
        else:
            self.pop[part_id].F = self.pop[part_id].old_F
        if random.random()<self.tau2:
            self.pop[part_id].CR = random.random()
        else:
            self.pop[part_id].CR = self.pop[part_id].old_CR
        r1 = random.randint(0, self.MAXSIZE-1)
        while r1 == part_id:
            r1 = random.randint(0, self.MAXSIZE-1)
        r2 = random.randint(0, self.MAXSIZE-1)
        while r2 == r1 or r2 == part_id:
            r2 = random.randint(0, self.MAXSIZE-1)
        r3 = random.randint(0, self.MAXSIZE-1)
        while r3 == r2 or r3 == r1 or r3 == part_id:
            r3 = random.randint(0, self.MAXSIZE-1)
        for j in range(self.MAXDIM):
            self.donor_vector[part_id].gene[j] = self.pop[r1].gene[j]+ self.pop[part_id].F *(self.pop[r2].gene[j]-self.pop[r3].gene[j])
            # 处理超出边界变量
            if self.donor_vector[part_id].gene[j] < self.lbound:
                self.donor_vector[part_id].gene[j] = 2 * self.lbound - self.donor_vector[part_id].gene[j]
                if self.donor_vector[part_id].gene[j] > self.rbound:
                    self.donor_vector[part_id].gene[j] = self.rbound
            if self.donor_vector[part_id].gene[j] > self.rbound:
                self.donor_vector[part_id].gene[j] = 2 * self.rbound - self.donor_vector[part_id].gene[j]
                if self.donor_vector[part_id].gene[j] < self.lbound:
                    self.donor_vector[part_id].gene[j] = self.lbound
            # while self.donor_vector[part_id].gene[j] < self.lbound or self.donor_vector[part_id].gene[j] > self.rbound:
            #     if self.donor_vector[part_id].gene[j] < self.lbound:
            #         self.donor_vector[part_id].gene[j] = 2 * self.lbound - self.donor_vector[part_id].gene[j]
            #     if self.donor_vector[part_id].gene[j] > self.rbound:
            #         self.donor_vector[part_id].gene[j] = 2 * self.rbound - self.donor_vector[part_id].gene[j]

    def crossover(self, part_id):
        for j in range(self.MAXDIM):
            jrand = random.randint(0, self.MAXDIM - 1)
            rand_val = random.random()
            if rand_val <= self.pop[part_id].CR or j == jrand:
                self.trial_vector[part_id].gene[j] = self.donor_vector[part_id].gene[j]
            else:
                self.trial_vector[part_id].gene[j] = self.pop[part_id].gene[j]
        self.trial_vector[part_id].fitness = self.calc_fitness(self.trial_vector[part_id].gene)
        self.trial_vector[part_id].F = self.pop[part_id].F
        self.trial_vector[part_id].CR = self.pop[part_id].CR
        if self.bestFitnessValue > self.trial_vector[part_id].fitness:
            self.bestFitnessValue = self.trial_vector[part_id].fitness
            self.bestParticleGene = self.trial_vector[part_id].gene

    def select(self, part_id):
        if self.trial_vector[part_id].fitness <= self.pop[part_id].fitness:
            self.pop[part_id].fitness = self.trial_vector[part_id].fitness
            for j in range(self.MAXDIM):
                self.pop[part_id].gene[j] = self.trial_vector[part_id].gene[j]
            self.pop[part_id].old_CR = self.pop[part_id].CR
            self.pop[part_id].old_F = self.pop[part_id].F

    def cd_select(self, pre_pop):
        '''
        通过拥挤度（crowding distance)结合快速非支配排序、精英选择策略，从当前及上一代两个种群中选择后代
        :param pre_pop:
        :return:
        '''
        # 将父代和子代合并
        combine_chromo = pre_pop + copy.deepcopy(self.pop)
        # 快速非支配排序
        F2, combine_chromo1 = CD.non_domination_sort(len(combine_chromo), combine_chromo)
        # 计算拥挤度进行排序
        combine_chromo2 = CD.crowding_distance_sort(F2, combine_chromo1)
        # 精英保留产生下一代种群
        chromo = CD.elitism(self.MAXSIZE, combine_chromo2)
        self.pop = chromo

    def ncd_select(self, pre_pop):
        '''
        使用ncd来选择下一代种群
        :param pre_pop:
        :return:
        '''
        combine_chromo = pre_pop + copy.deepcopy(self.pop)
        chromo = ncd(combine_chromo, self.MAXSIZE)
        self.pop = chromo

