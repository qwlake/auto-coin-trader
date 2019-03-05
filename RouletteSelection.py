import os
import random
import datetime
import logging

import pickle
import numpy as np
from matplotlib import pyplot as pt

####################################Columns80###################################

# log_path = os.path.dirname(os.path.abspath(__file__)) + '/log/rs.log'
# logging.basicConfig(filename=log_path,level=logging.DEBUG)
# logging.info(datetime.datetime.now())
# logging.info("RouletteSelection start")

np.set_printoptions(threshold=np.nan)

class RouletteSelection():
    TOP_N = 5
    MUTATION_RATE = 0.05
    def __init__(self, GeneticAlgorithm, highestPdNp, rateNp, opt=False):
                
        self.ndGenPool, self.ndNamePool, self.dataDic, self.taNameList, self.GENS, self.GENLEN = GeneticAlgorithm.return_inf()
        self.highestPdNp, self.rateNp = highestPdNp, rateNp
        self.top_index = np.argpartition(self.rateNp, -self.TOP_N)[-self.TOP_N:]
        self.opt = opt
        
    # def __init__(self, ndGenPool, ndNamePool, highestPdNp, rateNp,
    #              GENS, GENLEN):
    #     killIndexList = []
    #     for i, e in enumerate(highestPdNp):
    #         if e.returnProfit() < 100:
    #             killIndexList.append(i)
    #     self.ndGenPool = np.delete(ndGenPool, killIndexList, axis = 0)
    #     self.ndNamePool = np.delete(ndNamePool, killIndexList, axis = 0)
    #     self.highestPdNp = np.delete(highestPdNp, killIndexList)
    #     self.rateNp = np.delete(rateNp, killIndexList)
    #     self.GENS, self.GENLEN = GENS, GENLEN
    #     print("Degenerated gen kill",len(killIndexList))
        
    def double(self):
        fitness = self.rateNp.copy()
        doubledIndex = []
        doubled = []
        sumOfFitness = np.sum(fitness)
        for i in range(self.GENS*2):
            point = random.random()*sumOfFitness
            tempSum = 0
            for j, e2 in enumerate(fitness):
                tempSum = tempSum + e2
                if point < tempSum:
                    doubledIndex.append(j)
                    break
        for i in doubledIndex:
            doubled.append(fitness[i])
        return doubledIndex
    
    # def double(self):
    #     fitness = self.rateNp.copy()
    #     doubledIndex = []
    #     doubled = []
    #     sumOfFitness = np.sum(fitness)
    #     for i in range(self.GENS*2):
    #         point = random.random()*sumOfFitness
    #         tempSum = 0
    #         for j, e2 in enumerate(fitness):
    #             tempSum = tempSum + e2
    #             if point < tempSum:
    #                 doubledIndex.append(j)
    #                 break
    #     for i in doubledIndex:
    #         doubled.append(fitness[i])
    #     return doubledIndex
    
    def mutation(self, normal):
        for i, e in enumerate(normal):
            for j in range(0, self.MUTATION_RATE):
                temp = random.randint(0,np.shape(e)[0]-1)
                try:
                	e[temp] = random.random()
                except:
                    logging.info('random.randint(0,np.shape(e)[0])-1:{0}'.format(temp))
                    
    def mutation2(self, normal, name):
        target_index = random.randint(0,len(normal)-1)
        random_index = random.randint(0,np.shape(self.ndGenPool)[0]-1)
        taName = random.choice(self.taNameList)
        
        normal[target_index] = self.dataDic[taName]
        name[target_index] = taName
        return normal, name
    
    def singleMating(self, parentIndexList):
        crossPoint = []
        dad = self.ndGenPool[parentIndexList[0]]
        mom = self.ndGenPool[parentIndexList[1]]
        dadName = self.ndNamePool[parentIndexList[0]]
        momName = self.ndNamePool[parentIndexList[1]]
        child = []
        name = []
        for i in range(0, self.GENLEN):
            crossPoint.append(random.randint(0,1))
        for i, e in enumerate(crossPoint):
            if e == 1:
                child.append(dad[i])
                name.append(dadName[i])
            else:
                child.append(mom[i])
                name.append(momName[i])
        if self.opt:
            if random.random() <= self.MUTATION_RATE:
                child, name = self.mutation2(child, name)
        return child, name
    
    def mating(self, doubledIndex):
        DILen = len(doubledIndex)
        countTwo = 0
        popedIndexList = []
        children = self.ndGenPool[self.top_index].tolist()
        nameList = self.ndNamePool[self.top_index].tolist()
        # children = []
        # nameList = []
        # for i in range(0, DILen):   
        for i in range(0, DILen - self.TOP_N*2):    
            popPoint = random.randint(0, len(doubledIndex)-1)
            popedIndex = doubledIndex.pop(popPoint)
            popedIndexList.append(popedIndex)
            if countTwo%2 == 1:
                child, name = self.singleMating(popedIndexList)
                children.append(child)
                nameList.append(name)
                popedIndexList = []
            countTwo += 1
        newGen = np.array(children)
        newName = np.array(nameList)
        return newGen, newName

if __name__ == '__main__':
    pickle_path = os.path.dirname(os.path.abspath(__file__)) + '/pickle/roldata.pickle'
    with open(pickle_path, 'rb') as mypoldata:
        tempList = pickle.load(mypoldata)
    rol = RouletteSelection(tempList[0], tempList[1], tempList[2], tempList[3],
                            5000, 5, True)
    doubledIndex = rol.double()
    children = rol.mating(doubledIndex)
    
