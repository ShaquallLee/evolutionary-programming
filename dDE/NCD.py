#!/usr/bin/env python
# encoding: utf-8
# @author: lishaogang
# @file: NCD.py
# @time: 2020/7/8 0008 16:20
# @desc:new crowding distance,新拥挤距离在一维上的应用


def ncd(pop,N):
    '''
    使用新拥挤距离的方法从M个元素的种群中挑出N个下一代组成新的种群
    :param pop: 当前总的元素
    :param N:   最终留的元素个数
    :return:
    '''
    pop_sorted = sorted(pop, key=lambda item: item.fitness)
    pop_min = pop_sorted[0].fitness
    pop_max = pop_sorted[-1].fitness
    queue = [[0,len(pop_sorted)]]
    n = 2
    pop_selected = [pop_sorted[0], pop_sorted[-1]]
    while n < N and len(queue)>0:
        start, end = queue.pop(0)
        if start == end:
            continue
        cd_l = []
        for item in pop_sorted[start:end]:
            cd = ((item.fitness-pop_min)**2+(pop_max-item.fitness)**2)/(pop_max-pop_min)**2
            cd_l.append(cd)
        posi =cd_l.index(min(cd_l))
        queue.append([start, posi+start])
        queue.append([posi+start, end])
        pop_selected.append(pop_sorted[start+posi])
        n += 1
    return pop_selected



if __name__ == '__main__':
    pass
