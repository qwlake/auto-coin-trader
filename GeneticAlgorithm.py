import sys
import os
import random
import datetime
import time
import logging
import multiprocessing
from multiprocessing import Process, current_process, Queue, Pool

import pickle
import numpy as np
from matplotlib import pyplot as pt

import Analysis
import PastData
import RouletteSelection

####################################Columns80###################################

log_path = os.path.dirname(os.path.abspath(__file__)) + '/log/gen.log'
logging.basicConfig(filename=log_path,level=logging.DEBUG)

# multiprocessing.log_to_stderr()
# logger = multiprocessing.get_logger()
# logger.setLevel(logging.INFO)

def shape(a):
    return np.shape(a)

class GeneticAlgorithm():
    
    def __init__(self, 
                 analysis,  
                 GENERATION=100, 
                 GENS=100, 
                 GENLEN=5, 
                 FITPER=0.8,
                 PRS=2, 
                 PROFIT_RATE = 1.02,
                 ONE_DAY_TIME = 6,
                 SAFE_GUARD = 0.99,
                 opt=False):
        self.a = analysis
        self.dataDic, self.taNameList = self.a.returnData()
        self.chartData = self.a.returnChartData()
        
        self.GENERATION = GENERATION
        self.GENS = GENS
        self.GENLEN = GENLEN
        self.FITPER = FITPER
        self.PRS = PRS
        self.PROFIT_RATE = PROFIT_RATE
        self.ONE_DAY_TIME = ONE_DAY_TIME
        self.SAFE_GUARD = SAFE_GUARD
        self.opt = opt
        
        self.initGen()
        self.makeDailyUpDown()
        
    # def __del__(self):
    #     try:
    #         while(True):
    #             del self.pdnp[0]
    #     except:
    #         pass
    #     finally:
    #         del self.pdnp
    
    def return_inf(self):
        return (self.ndGenPool, self.ndNamePool, 
                self.dataDic, self.taNameList,
                self.GENS, self.GENLEN)
        
    def makeDailyUpDown(self):
        dailyUD = []
        count = 0
        for i, data in enumerate(self.chartData):
            if data['open'] < data['close']:
                dailyUD.append(1)
                count += 1
            else:
                dailyUD.append(0)
        print('Up days:',count)
        self.dailyUD = np.array(dailyUD)
        
    def simpleCal(self, pdList, gen):
        highestGen = pdList[0]
        highestRate = -9999
        highestProfit = 100
        for i, data in enumerate(pdList):
            flag = False
            flag_index = None
            profit = 100
            low, high = data.returnRange()
            for j,ud in enumerate(self.dailyUD[1700:]): ############################################
                try:
                    if self.SAFE_GUARD >= (self.chartData[j]['close']/
                                           self.chartData[flag_index]['open']):
                        profit *= (self.chartData[j]['close']/
                                   self.chartData[flag_index]['open'])
                        flag_index = None; flag = False
                except: pass
                mixed = gen[:,j]
                temp1, temp2 = (low<mixed), (high>mixed)
                if (temp1.sum()/temp1.size >= self.FITPER and 
                    temp2.sum()/temp2.size >= self.FITPER):
                    if not flag:
                        flag_index = j; flag = True
                else:
                    if flag:
                        flag = False
                        profit *= (self.chartData[j]['close']/
                                   self.chartData[flag_index]['open'])
            data.addProfit(profit)
            if highestProfit < profit:
                highestGen = data
                highestProfit = profit
        return highestGen, highestProfit
    
    def gathering(self, index, gen):
        pdList = []
        pop = gen[:,0]
        temp = PastData.PastData(pop, self.ndNamePool[index])
        pdList.append(temp)
        for j,ud in enumerate(self.dailyUD[:1700]): ############################################
            mixed = gen[:,j]
            isPdMatched = False
            for k, data in enumerate(pdList):
                low, high = data.returnRange()
                temp1, temp2 = (low<mixed), (high>mixed)
                if (temp1.sum()/temp1.size >= self.FITPER and temp2.sum()/temp2.size >= self.FITPER):
                    data.addData(mixed)
                    data.predictionDay(j)
                    isPdMatched = True
            if not isPdMatched:
                temp = PastData.PastData(mixed, self.ndNamePool[index])
                pdList.append(temp)
        return self.simpleCal(pdList, gen)
    
    # With Queues
    def calcualteFit(self, result = Queue(), returnPD = False):
        profitNp = np.empty([self.GENS], dtype='Float32')
        highestPdNp = np.empty([self.GENS], dtype=object)
        # lst = [0 for _ in range(10)]
        for i, g in enumerate(self.ndGenPool):
            highestGen, highestProfit = self.gathering(i, g)
            if returnPD:
                return highestGen
            profitNp[i] = highestProfit
            highestPdNp[i] = highestGen
            prName = current_process().name
            print("{0}'s Gen {1} cleared.".format(prName, i))
        profitIndex = np.argmax(profitNp)
        print('Rate', np.max(profitNp))
        print('UpFitness', highestPdNp[profitIndex].returnUpCount())
        print('DownFitness', highestPdNp[profitIndex].returnDownCount())
        
        # rateIndex = rateList.index(max(rateList))
        # print('Rate', max(rateList))
        # print('UpFitness', highestPdList[rateIndex].returnUpCount())
        # print('DownFitness', highestPdList[rateIndex].returnDownCount())
        
        # highestPdNp = np.array(highestPdList)
        # rateNp = np.array(rateList)
        
        return highestPdNp, profitNp
        
    def multiCalculate(self):
        tempC = int(self.GENS/self.PRS)
        pool = Pool(processes=self.PRS)
        result = pool.apply_async(self.calcualteFit, ())
        highestPdNp, profitNp = result.get()
        
        pool.close()
        pool.join()
            
        return highestPdNp, profitNp

    def initGen(self):
        pool = [0 for _ in range(self.GENS)]
        namePool = [0 for _ in range(self.GENS)]
        
        for i in range(self.GENS):
            tempPool = [0 for _ in range(self.GENLEN)]
            tempNamePool = [0 for _ in range(self.GENLEN)]
            for j in range(self.GENLEN):
                taName = random.choice(self.taNameList)
                tempPool[j] = self.dataDic[taName]
                tempNamePool[j] = taName
            pool[i] = tempPool
            namePool[i] = tempNamePool

        self.ndGenPool = np.array(pool)
        self.ndNamePool = np.array(namePool)

        print(shape(self.ndGenPool), shape(self.ndNamePool))
    
    def start(self):
        bestIndex = None
        bestName = None
        
        start_time = time.time()
        if self.PRS == -1:
            highestPdNp, profitNp = self.calcualteFit()
        else:
            highestPdNp, profitNp = self.multiCalculate()
        end_time = time.time() - start_time
        print("Generation {0} is end. Gen_End_Time: {1}".format(-1, end_time))
        
        start_time = time.time()
        maxProfit = np.max(profitNp)
        bestIndex = np.argmax(profitNp)
        bestName = self.ndNamePool[bestIndex]
        end_time = time.time() - start_time
        print("Searching End.: {0}".format(end_time))
        
        for i in range(0, self.GENERATION):
            rol = RouletteSelection.RouletteSelection(self, highestPdNp, profitNp, self.opt)
            # rol = RouletteSelection.RouletteSelection(
            #     self.ndGenPool, 
            #     self.ndNamePool, 
            #     highestPdNp, 
            #     profitNp,
            #     self.GENS, 
            #     self.GENLEN,
            # 	self.opt)
            doubledIndex = rol.double()
            
            start_time = time.time()
            self.ndGenPool, self.ndNamePool  = rol.mating(doubledIndex)
            end_time = time.time() - start_time
            # print("rol {0} is end. rol_End_Time: {1}".format(i, end_time))
            
            start_time = time.time()
            if self.PRS == -1:
                highestPdNp, profitNp = self.calcualteFit()
            else:
                highestPdNp, profitNp = self.multiCalculate()
            end_time = time.time() - start_time
#            print("Generation {0} is end. Gen_End_Time: {1}".format(i, end_time))
            if np.max(profitNp) > maxProfit:
                maxProfit = np.max(profitNp)
                bestIndex = np.argmax(profitNp)
                bestName = self.ndNamePool[bestIndex]
                
                # logging.info("Gen {0} bestName {1}".format(i, bestName))
                
                print("maxProfit has been changed.")
            print("Gen {0} is end.".format(i))
            print("maxProfit: ", maxProfit)
            print("Average: ", np.mean(np.array(profitNp)))
            
        print(bestName)
        
        # Use pickle
        tempList = [self.ndGenPool, self.ndNamePool, highestPdNp, profitNp]
        pickle_path = os.path.dirname(os.path.abspath(__file__)) + '/pickle/roldata.pickle'
        with open(pickle_path, 'wb') as myroldata:
            roldata = pickle.dump(tempList, myroldata)

        return bestName, maxProfit
            
if __name__ == '__main__':
    
    start_time = time.time()
    an = Analysis.Analysis()
    ga = GeneticAlgorithm(an, GENERATION=100, GENS=100, PRS=-1, opt=True)
    bestName, maxProfit = ga.start()
    end_time = time.time() - start_time
    print('Time', end_time)
    logging.info(datetime.datetime.now())
    logging.info('Non mutation.')
    logging.info('GENERATION:   {0}'.format(ga.GENERATION))
    logging.info('GENS:         {0}'.format(ga.GENS))
    logging.info('GENLEN:       {0}'.format(ga.GENLEN))
    logging.info('FITPER:       {0}'.format(ga.FITPER))
    logging.info('PROFIT_RATE:  {0}'.format(ga.PROFIT_RATE))
    logging.info('ONE_DAY_TIME: {0}'.format(ga.ONE_DAY_TIME))
    logging.info("End time:     {0}".format(datetime.datetime.now()))
    logging.info("Run time:     {0} seconds".format(end_time))
    logging.info("Max Profit:   {0} \n".format(maxProfit))
    
    pickle_path = os.path.dirname(os.path.abspath(__file__)) + '/pickle/profittest.pickle'
    with open(pickle_path, 'wb') as mypoldata:
        pickle.dump(ga, mypoldata)          # ga = GeneticAlgorithm
        pickle.dump(an, mypoldata)          # an = Analysis
        pickle.dump(bestName, mypoldata)	# bestName = ga.start()
        
        