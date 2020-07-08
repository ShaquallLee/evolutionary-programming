#!/usr/bin/env python
# encoding: utf-8
# @author: lishaogang
# @file: CD.py
# @time: 2020/7/7 0007 10:16
# @desc: crowding distance 拥挤距离的计算

import numpy as np

def non_domination_sort(N,chromo):
    #non_domination_sort 初始种群的非支配排序和计算拥挤度
    #初始化pareto等级为1
    pareto_rank=1
    F={}#初始化一个字典
    F[pareto_rank]=[]#pareto等级为pareto_rank的集合
    pn={}
    ps={}
    for i in range(N):
        #计算出种群中每个个体p的被支配个数n和该个体支配的解的集合s
        pn[i]=0#被支配个体数目n
        ps[i]=[]#支配解的集合s
        for j in range(N):
            if i == j:
                continue
            if chromo[i].fitness < chromo[j].fitness:
                ps[i].append(j)
            elif chromo[i].fitness > chromo[j].fitness:
                pn[i] += 1
        if (pn[i]==0):
            chromo[i].paretorank=1#储存个体的等级信息
            F[pareto_rank].append(i)
    #求pareto等级为pareto_rank+1的个体
    while (len(F[pareto_rank])!=0):
        temp=[]
        for i in range(len(F[pareto_rank])):
            if (len(ps[F[pareto_rank][i]])!=0):
                for j in range(len(ps[F[pareto_rank][i]])):
                    pn[ps[F[pareto_rank][i]][j]]=pn[ps[F[pareto_rank][i]][j]]-1#nl=nl-1
                    if pn[ps[F[pareto_rank][i]][j]]==0:
                        chromo[ps[F[pareto_rank][i]][j]].paretorank=pareto_rank+1#储存个体的等级信息
                        temp.append(ps[F[pareto_rank][i]][j])
        pareto_rank=pareto_rank+1
        F[pareto_rank]=temp
    return F,chromo


def crowding_distance_sort(F,chromo_non):
    #计算拥挤度
    ppp=[]
    #按照pareto等级对种群中的个体进行排序
    temp=sorted(chromo_non,key=lambda Individual:Individual.paretorank)#按照pareto等级排序后种群
    index1=[]
    for i in range(len(temp)):
        index1.append(chromo_non.index(temp[i]))
    #对于每个等级的个体开始计算拥挤度
    current_index = 0
    for pareto_rank in range(len(F)-1):#计算F的循环时多了一次空，所以减掉,由于pareto从1开始，再减一次
        nd=np.zeros(len(F[pareto_rank+1]))#拥挤度初始化为0
        y=[]#储存当前处理的等级的个体
        for i in range(len(F[pareto_rank+1])):
            y.append(temp[current_index + i])
        current_index=current_index + i + 1
        #对于每一个目标函数fm
        for i in range(1):
            #根据该目标函数值对该等级的个体进行排序
            index_objective=[]#通过目标函数排序后的个体索引
            objective_sort=sorted(y,key=lambda Individual:Individual.fitness)#通过目标函数排序后的个体
            for j in range(len(objective_sort)):
                index_objective.append(y.index(objective_sort[j]))
            #记fmax为最大值，fmin为最小值
            fmin=objective_sort[0].fitness
            fmax=objective_sort[len(objective_sort)-1].fitness
            #对排序后的两个边界拥挤度设为1d和nd设为无穷
            nd[index_objective[0]]=float("inf")
            nd[index_objective[len(index_objective)-1]]=float("inf")
            #计算nd=nd+(fm(i+1)-fm(i-1))/(fmax-fmin)
            j=1
            while (j<=(len(index_objective)-2)):
                pre_f=objective_sort[j-1].fitness
                next_f=objective_sort[j+1].fitness
                if (fmax-fmin==0):
                    nd[index_objective[j]]=float("inf")
                else:
                    nd[index_objective[j]]=float((next_f-pre_f)/(fmax-fmin))
                j=j+1
        for i in range(len(y)):
            y[i].nnd=nd[i]
            ppp.append(y[i])
    return ppp


def elitism(N,combine_chromo2):
    '''
    根据精英策略选择较优个体
    :param N:
    :param combine_chromo2:
    :return:
    '''
    chromo=[]
    #根据pareto等级从小到大进行排序
    chromo_rank=sorted(combine_chromo2,key=lambda Individual:Individual.paretorank, reverse=False)
    chromo_rank_class = {}
    for x in chromo_rank:
        if x.paretorank not in chromo_rank_class.keys():
            chromo_rank_class[x.paretorank] = [x]
        else:
            chromo_rank_class[x.paretorank].append(x)
    i = 0
    n = N
    for rank, items in chromo_rank_class.items():
        if len(items) <= n:
            chromo+=items
            n -= len(items)
        else:
            chromo_cd = sorted(items, key=lambda Individual:Individual.ndd, reverse=True)
            chromo += chromo_cd[:n]
            break
    return chromo