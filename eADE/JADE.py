import math

from eADE.Particle import Particle
import random
import copy


class JADE():
    def __init__(self, MAXSIZE, MAXDIM, MAXGEN, calc_fitness, lbound, rbound,mu_CR=0.5,mu_F=0.5, p=0.05, c=0.1):
        self.MAXSIZE = MAXSIZE
        self.MAXDIM = MAXDIM
        self.MAXGEN = MAXGEN
        self.lbound = lbound
        self.rbound = rbound
        self.mu_CR = mu_CR
        self.mu_F = mu_F
        self.p = p
        self.c = c
        self.calc_fitness = calc_fitness
        self.pop = [Particle(MAXDIM,lbound,rbound, calc_fitness) for i in range(MAXSIZE)]    #初始种群
        self.donor_vector = [Particle(MAXDIM, lbound, rbound, calc_fitness) for i in range(MAXSIZE)]
        self.trial_vector = [Particle(MAXDIM, lbound, rbound, calc_fitness) for i in range(MAXSIZE)]
        self.archive_vector = []
        self.archive_size =MAXSIZE
        self.archive_count = 0
        self.bestFitnessValue = self.pop[0].fitness
        self.bestFitnessValues = []

        self.indexes = [i for i in range(MAXSIZE)]
        self.deviateAvaliable = False
        self.storedDeviate = 0

    def update_bestfitness(self):
        best = self.pop[0]
        for i in range(1, self.MAXSIZE):
            if best.fitness > self.pop[i].fitness:
                best = self.pop[i]
        self.bestFitnessValue = best.fitness
        self.bestFitnessValues.append(best.fitness)

    def quickselect(self, begin, end, k):
        '''
        快速选出population中indexes从begin到end之间的前K个元素
        :param begin:
        :param end:
        :param k:
        :return:
        '''
        if k<=0 or begin >= end:
            return 0
        i = begin
        j = end
        sa = 0

        tmp = self.pop[self.indexes[begin]].fitness
        tmp_index = self.indexes[begin]

        while i != j:
            while j >i and self.pop[self.indexes[j]].fitness > tmp:
                j -=1
            self.indexes[i] = self.indexes[j]
            while i < j and self.pop[self.indexes[i]].fitness <= tmp:
                i += 1
            self.indexes[j] = self.indexes[i]
        self.indexes[i] = tmp_index

        sa = i - begin+1
        if sa < k:
            self.quickselect(i+1, end, k-sa)
        elif sa > k:
            self.quickselect(begin, i-1, k)
        else:
            return 0


    def update(self):
        self.update_bestfitness()
        for i in range(self.MAXGEN):
            for j in range(self.MAXSIZE):
                self.update_parameters(j)
            self.quickselect(0, self.MAXSIZE-1, int(math.ceil(self.p*self.MAXSIZE)))
            for j in range(self.MAXSIZE):
                self.mutation(j)
            for j in range(self.MAXSIZE):
                self.crossover(j)
            self.select()
            self.bestFitnessValues.append(self.bestFitnessValue)


    def mutation(self, part_id):
        pbest = self.indexes[random.randint(0, math.ceil(self.p*self.MAXSIZE))]
        r1 = random.randint(0, self.MAXSIZE-1)
        while r1 == part_id:
            r1 = random.randint(0, self.MAXSIZE-1)
        r2 = random.randint(0, self.MAXSIZE-1)
        while r2 == r1 or r2 == part_id:
            r2 = random.randint(0, self.MAXSIZE-1)

        for j in range(self.MAXDIM):
            self.donor_vector[part_id].gene[j] = self.pop[part_id].gene[j]+\
                                                 self.pop[part_id].F*(self.pop[pbest].gene[j]-self.pop[part_id].gene[j])+\
                                                 self.pop[part_id].F*(self.pop[r1].gene[j]-self.pop[r2].gene[j])
            # 处理超出边界变量
            if self.donor_vector[part_id].gene[j] < self.lbound:
                self.donor_vector[part_id].gene[j] = (self.pop[part_id].gene[j]+self.lbound)/2
            if self.donor_vector[part_id].gene[j] > self.rbound:
                self.donor_vector[part_id].gene[j] = (self.pop[part_id].gene[j]+self.rbound)/2
            # if self.donor_vector[part_id].gene[j] < self.lbound:
            #     self.donor_vector[part_id].gene[j] = 2 * self.lbound - self.donor_vector[part_id].gene[j]
            #     if self.donor_vector[part_id].gene[j] > self.rbound:
            #         self.donor_vector[part_id].gene[j] = self.rbound
            # if self.donor_vector[part_id].gene[j] > self.rbound:
            #     self.donor_vector[part_id].gene[j] = 2 * self.rbound - self.donor_vector[part_id].gene[j]
            #     if self.donor_vector[part_id].gene[j] < self.lbound:
            #         self.donor_vector[part_id].gene[j] = self.lbound
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

    def select(self):
        S_CR = 0
        S_F = 0
        S_F2 = 0
        success_count =0
        for i in range(self.MAXSIZE):
            if self.trial_vector[i].fitness<self.pop[i].fitness:
                S_CR += self.pop[i].CR
                S_F += self.pop[i].F
                S_F2 += self.pop[i].F**2
                success_count += 1
                if self.archive_size > 0:
                    index = self.archive_count
                    if index >= self.archive_size:
                        index = random.randint(0, self.archive_size)
                        self.archive_vector[index] = self.pop[i]
                    else:
                        self.archive_vector.append(self.pop[i])
                        self.archive_count += 1
                self.pop[i] = self.trial_vector[i]
        if success_count > 0:
            self.mu_CR = (1-self.c)*self.mu_CR+self.c*(S_CR/success_count)
            self.mu_F = (1-self.c)*self.mu_F+self.c*(S_F2/S_F)

    def update_parameters(self, part_id):
        self.pop[part_id].CR = self.genrand_normal(self.mu_CR, 0.1)

        if self.pop[part_id].CR > 1:
            self.pop[part_id].CR = 1
        if self.pop[part_id].CR < 0:
            self.pop[part_id].CR = 0

        self.pop[part_id].F = self.genrand_cauchy(self.mu_F, 0.1)
        while self.pop[part_id].F < 0:
            self.pop[part_id].F = self.genrand_cauchy(self.mu_F, 0.1)
        if self.pop[part_id].F > 1:
            self.pop[part_id].F = 1


    def genrand_cauchy(self, alpha, beta):
        return alpha+beta*math.tan(math.pi*(random.random()-0.5))

    def genrand_normal(self, mu=0.0, sigma=1.0):
        # deviateAvaliable = False
        if not self.deviateAvaliable:
            var1= 2.0*random.random()-1.0
            var2 = 2.0*random.random()-1.0
            rsquared = var1*var1+var2*var2
            while rsquared>=1 or rsquared == 0:
                var1 = 2.0 * random.random() - 1.0
                var2 = 2.0 * random.random() - 1.0
                rsquared = var1 * var1 + var2 * var2
            polar = math.sqrt(-2.0*math.log10(rsquared)/rsquared)

            self.storedDeviate = var1*polar
            self.deviateAvaliable = True
            return var2*polar*sigma+mu
        else:
            self.deviateAvaliable = False
            return self.storedDeviate*sigma+mu
