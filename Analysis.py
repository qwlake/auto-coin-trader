import os
import time
import datetime
import re

import talib
from talib import abstract
from matplotlib import pyplot as pt
import numpy as np
import pickle

import ROAPI

####################################Columns80###################################

np.set_printoptions(threshold=np.nan)

class Analysis():
    
    THREE_DAY_TIME = 18
    usable_ta_numbers = 0
    
    def __init__(self):
        pickle_path = os.path.dirname(os.path.abspath(__file__)) + '/pickle/poldata.pickle'
        with open(pickle_path, 'rb') as mypoldata:
            self.data = pickle.load(mypoldata)
            
        #############################################################
        # # When Pickle is running, This is usless.
        # now = datetime.datetime.now()
        # past = now.replace(year=now.year-1)
        # startStamp = datetime.datetime.timestamp(past)
        # endStamp = datetime.datetime.timestamp(now)
        # period = 14400
        # # period examples: 300, 900, 1800, 7200, 14400, and 86400
        
        # currency = "USDT_BTC"
        # x = ROAPI.poloniex()
        # self.data = x.returnChartData(currency,startStamp,endStamp,period)
        #############################################################

        weightedAverage = []
        openList = []
        highList = []
        lowList = []
        closeList = []
        volumeList = []
        
        for i in self.data:
            for j,k in i.items():
                if j == 'weightedAverage':
                    weightedAverage.append(k)
                elif j == 'open':
                    openList.append(k)
                elif j == 'high':
                    highList.append(k)
                elif j == 'low':
                    lowList.append(k)
                elif j == 'close':
                    closeList.append(k)
                elif j == 'volume':
                    volumeList.append(k)
        
        self.nparray = {'open':np.array(openList),'high':np.array(highList),
                   'low':np.array(lowList),'close':np.array(closeList),
                   'volume':np.array(volumeList),'period':self.THREE_DAY_TIME//3}
        self.dataDic = {}
        self.taNameList = []
        
        # pickle_path = os.path.dirname(os.path.abspath(__file__)) + '/pickle/poldata.pickle'
        # with open(pickle_path, 'wb') as mypoldata:
        #     self.poldata = pickle.dump(self.data, mypoldata)
        
    # Returns a data that is loaded by pickling.
    # The data is loaded from Poloniex's API server, and it's about "USDT_BTC".
    # The data has Poloniex's ChartData of last one year with unfixed period(now on 14400).
    # Input: -
    # Output: List [{'open':0,'high':0,'low':0,'close':0,...},...]
    def returnChartData(self):
        return self.data[self.THREE_DAY_TIME:]

    # Classify input number.
    # Input: Any number
    # Output: True, False
    def isNumber(self,num):
        try:
            judge = str(float(num))
            return (False if(judge=='nan' or judge=='inf' or judge =='-inf') 
                    else True)
        except (ValueError,TypeError):
            return False    
    
    # Returns maximum number of inputed list
    # Input: array-like messData / will be judged array-like
    # Output: Float largest number
    #         False IndexError
    def largest(self, messData=np.ndarray):       
        try:
            return np.max(messData)
        except TypeError:
            return False

    # Returns minimum number of inputed list
    # Input: array-like messData / will be judged array-like
    # Output: Float smallest number
    #         False IndexError
    def smallest(self, messData=np.ndarray):
        try:
            return np.min(messData)
        except TypeError:
            return False
        
    # Filter -1 of npData that is means NaN or inf or -inf of all 0.
    # Edits dataDic and taNameList made of rests.
    # Input: array-like npData / taName's Value
    #        String taName / taName
    # Output: -
    def listMake(self, npData, taName):
        try:
            if npData == -1:
                # print ("This is NaN or inf or All 0")
                pass
            if not npData:
                # print ("This is NaN or inf or All 0")
                pass
        except:
            pass
        else: 
            # print (type(normaled),normaled)
            # npData = np.array(normaled)
            self.dataDic[taName] = npData
            self.taNameList.append(taName)
            self.usable_ta_numbers += 1
                            
            '''Show Graph'''
            # print(taName)
            # print (npData)
            # pt.plot(npData)
            # pt.show()
    
    def bbandsNormalization(self, upper, middle, lower):
        if not len(upper) == len(middle) == len(lower):
            return -1
        upper = upper - lower
        middle = middle - lower
        lower = np.zeros_like(lower)
        with np.errstate(divide='ignore'):
        	middle = middle / upper
        isfinite = np.invert(np.isfinite(middle))
        middle[isfinite] = 0
        
        downIndex = middle < 0
        upIndex = middle > 1
        middle[downIndex] = 0
        middle[upIndex] = 1

        print(type(middle))
        return middle
    
    def normalization(self,messData=np.ndarray):
        mD_len = len(messData)	# Ckeck point
        validIndex = 0
        for i,e in enumerate(messData):
            if not self.isNumber(e):
                messData[i] = 0
            else:
                validIndex = i
                break
        minValue = self.smallest(messData[validIndex:])
        messData[validIndex:] = messData[validIndex:].copy() - minValue
        maxValue = self.largest(messData)
        
        with np.errstate(invalid='ignore'):
        	messData = messData/maxValue
            
        minValue = self.smallest(messData)
        maxValue = self.largest(messData)
        
        if (not np.isfinite(minValue) or 
            not np.isfinite(maxValue) or 
            minValue != 0 or 
            maxValue != 1):
            return -1
        
        # # Check Purity
        # if minValue != 0 or maxValue != 1:
        #     print (messData)
        # 	print('maxValue: ',maxValue,'\n','minValue: ',minValue)
        #     pt.plot(evaluated)
        #     pt.show()
        if mD_len != len(messData):
            print("evaluated is invalid")
            
        return messData

    # Slice array in the input dictionary with point.
    # Slice range is from 'point-18'(It means 3 days ago) to point.
    # Input: Dictionary dic / {'open':ndarray[1,2,3,...],...}
    #        Integer point / over 18 number (18 means 3 days).
    # Output: Dictionary same as input dictionary, but is sliced with point.
    def sliceDic(self, startIndex=0, endIndex=18):
        sliced = {}
        for k, value in self.nparray.items():
            if not isinstance(value, int):
            	sliced[k] = value[startIndex:endIndex].copy()
        return sliced
    
    def taReturnThree(self, taName):
        if taName == 'BBANDS':
            concat = []
            for i in range(self.THREE_DAY_TIME, len(self.nparray['open'])):
                sliced = self.sliceDic(i-self.THREE_DAY_TIME, i)
                ta = abstract.Function(taName)
                ta.set_input_arrays(sliced)
                orgData = ta(self.THREE_DAY_TIME//3, 2, 2, 1)
                # print(orgData,'###')
                normaled = self.bbandsNormalization(
                    orgData[0], self.nparray['close'].copy(), orgData[2])
                try:
                	concat.append(normaled[-1].copy())
                except TypeError:
                	concat = normaled; return
            # print('taReturnThree concat:',concat)
            self.listMake(concat, taName)
    
    def taReturnTwo(self, taName):
        if taName == 'MAMA':
            return
        concat1 = []
        concat2 = []
        for i in range(self.THREE_DAY_TIME, len(self.nparray['open'])):
            sliced = self.sliceDic(i-self.THREE_DAY_TIME, i)
            ta = abstract.Function(taName)
            ta.set_input_arrays(sliced)
            orgData = ta(self.THREE_DAY_TIME//3)
            # print(orgData,'###')
            normaled1 = self.normalization(orgData[0])
            normaled2 = self.normalization(orgData[1])
            try:
            	concat1.append(normaled1[-1].copy())
            	concat2.append(normaled2[-1].copy())
            except TypeError:
                concat1, concat2 = normaled1, normaled2; return
        # print('taReturnTwo concat1:',concat1)
        # print('taReturnTwo concat2:',concat2)
        self.listMake(concat1, taName)
        self.listMake(concat2, taName)
        
    def taReturnOne(self, taName):
        concat = []
        for i in range(self.THREE_DAY_TIME, len(self.nparray['open'])):
            sliced = self.sliceDic(i-self.THREE_DAY_TIME, i)
            ta = abstract.Function(taName)
            ta.set_input_arrays(sliced)
            orgData = ta(self.THREE_DAY_TIME//3)
            normaled = self.normalization(orgData)
            try:
            	concat.append(normaled[-1].copy())
            except TypeError:
                concat = normaled; return
        self.listMake(concat, taName)
    
    def returnData(self):
        functions = talib.get_functions()
        count = 0
        p = re.compile('CDL.')
        
        for fun in functions:
            taName = fun
            CDL_Matched = p.match(taName)
            if CDL_Matched:         continue
            if taName == 'MAVP': 	continue
                   
            sliced = self.sliceDic()
            ta = abstract.Function(taName)
            ta.set_input_arrays(sliced)
                           
            if taName == 'MAMA': 	orgData = ta()
            else:                   orgData = ta(6)
            if isinstance(orgData, np.ndarray):
                self.taReturnOne(taName)
            
            elif len(orgData) == 2:
                self.taReturnTwo(taName)
                    
            elif len(orgData) == 3:
                self.taReturnThree(taName)

        print('Usable TA numbers:', self.usable_ta_numbers)
        return self.dataDic, self.taNameList
    
if __name__ == '__main__':
    start = Analysis()
    start.returnData()
