import numpy as np

####################################Columns80###################################

class PastData():
    
    RANGE = 0.1
    
    def __init__(self, ndGen, taName):
        self.genList = [ndGen]
        self.ndGen = ndGen
        self.taName = taName
        self.uCount = 1
        self.dCount = 0
        self.upDay = []
        self.upPoint = []
        
    def returnRange(self):
        return self.ndGen-self.RANGE, self.ndGen+self.RANGE
    
    def returnDay(self):
        return self.upDay
    
    def returnRate(self):
        u, d = self.uCount, self.dCount
        return np.log(u+2)/np.log10(d+u+2)*u-d
    
    def returnProfit(self):
        return self.profit
    
    def returnUpCount(self):
        return self.uCount
    
    def returnDownCount(self):
        return self.dCount
    
    def returnGen(self):
        return self.ndGen
    
    def returnTaName(self):
        return self.taName
    
    def predictionDay(self, up):
        self.upDay.append(up)
        self.upDay.sort()
        
    def recordPoint(self, point):
        self.upPoint.append(point)
        self.pointAvr = sum(self.upPoint)/len(self.upPoint)
    
    def upCount(self):
        self.uCount += 1
        
    def downCount(self):
        self.dCount += 1
        
    def addData(self, data):
        self.upCount()
        self.genList.append(data)
#        self.ndGen = (self.ndGen+(data/self.count)) / self.count

    def addProfit(self, profit):
        self.profit = profit
        
    def genPrint(self):
#        print(self.genList)
        print('upCount',self.uCount)
        print('downCount',self.dCount)
        
#        ndGenList = np.array(self.genList)
#        for i in ndGenList:
#            pt.plot(i)
#        pt.show()

#        print(self.taName)
#        print(ndGenList)
#        print(shape(ndGenList))