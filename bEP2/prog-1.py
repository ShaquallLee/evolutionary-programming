#!/usr/bin/env python
# encoding: utf-8
# @author: lishaogang
# @file: prog.py
# @time: 2020/6/22 0022 17:54
# @desc: test2
import copy
import random
import test_functions as tfs
import matplotlib.pyplot as plt

POPSIZE=100
MAXGENS=500
NVARS=30
PXOVER=0.8
PMUTATION=0.001

generation=0
cur_best = None

class genotype():
    def __init__(self, gene, fitness, upper, lower, rfitness, cfitness):
        self.gene = gene
        self.fitness = fitness
        self.upper = upper
        self.lower = lower
        self.rfitness = rfitness
        self.cfitness = cfitness

population = []
newpopulation = []

def initialize(lbound, ubound):
    first = True
    with open("gadata-2.txt", "r") as f:
        for i in range(NVARS):
            # line = f.readline()
            # lbound, ubound = map(float, line.rstrip().split(','))
            for j in range(POPSIZE):
                if first:
                    geno = genotype([0] * NVARS, 0, [0] * NVARS, [0] * NVARS, 0, 0)
                    geno.lower[i] = lbound
                    geno.upper[i] = ubound
                    geno.gene[i] = randval(lbound, ubound)
                    population.append(geno)
                else:
                    population[j].fitness = 0
                    population[j].rfitness = 0
                    population[j].cfitness = 0
                    population[j].lower[i] = lbound
                    population[j].upper[i] = ubound
                    population[j].gene[i] = randval(lbound, ubound)
            first = False
    for j in range(POPSIZE+1):
        newpopulation.append(genotype([0] * NVARS, 0, [0] * NVARS, [0] * NVARS, 0, 0))

def randval(low, high):
    num = random.uniform(low, high)
    return round(num, 3)

def evaluate(func):
    x = [None]*NVARS
    for mem in range(POPSIZE):
        for i in range(NVARS):
            x[i] = population[mem].gene[i]
        population[mem].fitness = func(x)

def keep_the_best():
    cur_best = 0
    population.append(copy.deepcopy(population[0]))
    for mem in range(POPSIZE):
        if population[mem].fitness < population[POPSIZE].fitness:
            cur_best = mem
            population[POPSIZE].fitness = population[mem].fitness
    for i in range(NVARS):
        population[POPSIZE].gene[i] = population[cur_best].gene[i]

def elitist():
    best = population[0].fitness
    worst = population[0].fitness
    for i in range(POPSIZE-1):
        if population[i].fitness > population[i+1].fitness:
            if population[i].fitness >= best:
                best = population[i].fitness
                best_mem = i
            if population[i+1].fitness <= worst:
                worst = population[i+1].fitness
                worst_mem = i+1
        else:
            if population[i].fitness <= worst:
                worst = population[i].fitness
                worst_mem = i
            if population[i+1].fitness >= best:
                best = population[i+1].fitness
                best_mem = i+1

    if worst <= population[POPSIZE].fitness:
        for i in range(NVARS):
            population[POPSIZE].gene[i] = population[worst_mem].gene[i]
        population[POPSIZE].fitness = population[worst_mem].fitness
    else:
        for i in range(NVARS):
            population[best_mem].gene[i] = population[POPSIZE].gene[i]
        population[best_mem].fitness = population[POPSIZE].fitness

def select():
    sum = 0
    for mem in range(POPSIZE):
        sum += population[mem].fitness

    for mem in range(POPSIZE):
        population[mem].rfitness = population[mem].fitness/sum
    population[0].cfitness = population[0].rfitness
    for mem in range(1, POPSIZE):
        population[mem].cfitness = population[mem-1].cfitness+population[mem].rfitness

    for i in range(POPSIZE):
        p = random.random()
        if p < population[0].cfitness:
            newpopulation[i] = population[0]
        else:
            for j in range(POPSIZE):
                if p >= population[j].cfitness and \
                        p < population[j+1].cfitness:
                    newpopulation[i] = population[j+1]

    for i in range(POPSIZE):
        population[i] = newpopulation[i]

def crossover():
    first = 0
    for mem in range(POPSIZE):
        x = random.random()
        if x < PXOVER:
            first += 1
            if first %2 == 0:
                Xover(one, mem)
            else:
                one = mem

def Xover(one, two):
    if NVARS > 1:
        if NVARS == 2:
            point = 1
        else:
            point = random.randint(0, NVARS-1)
        for i in range(point):
            population[one].gene[i], population[two].gene[i] = population[two].gene[i], population[one].gene[i]

def mutate():
    for i in range(POPSIZE):
        for j in range(NVARS):
            x = random.random()
            if x < PMUTATION:
                lbound = population[i].lower[j]
                ubound = population[i].upper[j]
                population[i].gene[j] = randval(lbound, ubound)

def report():
    sum = 0.0
    sum_square = 0.0
    for i in range(POPSIZE):
        sum += population[i].fitness
        sum_square += population[i].fitness * population[i].fitness
    avg = sum/POPSIZE
    square_sum = avg*avg*POPSIZE
    sqrt_num = (sum_square-square_sum)/(POPSIZE-1)
    # stddev = math.sqrt(sqrt_num)
    stddev = sqrt_num**0.5
    best_val = population[POPSIZE].fitness
    print("{}: {}, {}, {}".format(generation, best_val, avg, stddev))


if __name__ == '__main__':
    # n = 30
    # bf_sum = 0.0
    # for i in range(n):
    #     generation = 0
    #     population = []
    #     newpopulation = []
    fitnesses = []
    initialize(-100,100)
    evaluate(tfs.f3)
    keep_the_best()
    while generation < MAXGENS:
        generation += 1
        select()
        crossover()
        mutate()
        report()
        fitnesses.append(population[POPSIZE].fitness)
        evaluate(tfs.f3)
        elitist()
        # print(i+1, "：", population[POPSIZE].fitness)
        # bf_sum += population[POPSIZE].fitness
    plt.plot(fitnesses)
    plt.show()
    print("simulation completed")
    print("best fitness:", population[POPSIZE].fitness)
    print("Success!")
