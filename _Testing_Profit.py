import os

import pickle
import numpy as np
from matplotlib import pyplot as pt

class ProfitTest():
    def __init__(self, genalgo, analysis, bestName):
        self.money = 100
        self.ga = genalgo
        self.a = analysis
        self.bestName = bestName

    def initGen(self):
        dataDic, taNameList = self.a.returnData()
        addDem = []
        pool = []
        for i in self.bestName[0]:
            pool.append(dataDic[i])
        addDem.append(pool)
        ndGenPool = np.array(addDem)
                
        # Check the Types
#        print(type(ndGenPool), type(ndGenPool[0]), type(ndGenPool[0][0]))
#        print(type(self.bestName), type(self.bestName[0]))

        print(np.shape(ndGenPool),np.shape(self.bestName))
        
        return ndGenPool
    
    def fun1(self, ndGenPool, bestName, dailyUD):
        moneyHistory = []
        chartDataList = self.a.returnChartData()
        pd = self.ga.calcualteFit(ndGenPool, bestName, dailyUD, chartDataList,
                                  returnPD = True)
        upDay = pd.returnDay()
        print(upDay)
        
        for upIndex in upDay:
            changeRate = (chartDataList[upIndex+1]['open']/
                          chartDataList[upIndex]['close'])
            self.money *= changeRate
            moneyHistory.append(self.money)
            
        pt.plot(moneyHistory)
        pt.show()
    
if __name__ == '__main__':
    pickle_path = os.path.dirname(os.path.abspath(__file__)) + '/pickle/profittest.pickle'
    with open(pickle_path, 'rb') as mypoldata:
        ga = pickle.load(mypoldata)
        an = pickle.load(mypoldata)
        bestName = pickle.load(mypoldata)
    pft = ProfitTest(ga, an, bestName)
    ndGenPool = pft.initGen()
    dailyUD = pft.ga.makeDailyUpDown()
    pft.fun1(ndGenPool, bestName, dailyUD)
    
