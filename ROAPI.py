#import urllib
import requests
from urllib.request import urlopen
import json
import time
import codecs

def createTimeStamp(datestr, format="%Y-%m-%d %H:%M:%S"):
    return time.mktime(time.strptime(datestr, format))

class poloniex:
    def __init__(self):
        pass

    def api_query(self, req={}):
        reader = codecs.getreader("utf-8")
        
        requests.get('https://poloniex.com/public', params=req)

        if(req["command"] == "returnTicker" or req["command"] == "return24Volume"):
            preRet = requests.get('https://poloniex.com/public', params=req)
            ret = urlopen(preRet.url)
            return json.load(reader(ret))
        elif(req["command"] == "returnOrderBook"):
            preRet = requests.get('https://poloniex.com/public', params=req)
            ret = urlopen(preRet.url)
            return json.load(reader(ret))
        elif(req["command"] == "returnTradeHistory"):
            preRet = requests.get('https://poloniex.com/public', params=req)
            ret = urlopen(preRet.url)
            return json.load(reader(ret))

        elif(req["command"] == "returnTradeHistory2"):
            preRet = requests.get('https://poloniex.com/public', params=req)
            ret = urlopen(preRet.url)
            return json.load(reader(ret))
        
        elif(req["command"] == "returnChartData"):
            preRet = requests.get('https://poloniex.com/public', params=req)
            ret = urlopen(preRet.url)
            return json.load(reader(ret))
        else:
            print("Command is wrong.")


    def returnTicker(self):
        return self.api_query("returnTicker")

    def return24Volume(self):
        return self.api_query("return24Volume")

    def returnOrderBook (self, currencyPair):
        return self.api_query("returnOrderBook", {'currencyPair': currencyPair})

    def returnMarketTradeHistory (self, currencyPair):
        return self.api_query("returnMarketTradeHistory", 
                              {'currencyPair': currencyPair})

    # Returns your open orders for a given market, specified by the "currencyPair" POST parameter, e.g. "BTC_XCP"
    # Inputs:
    # currencyPair  The currency pair e.g. "BTC_XCP"
    # Outputs: 
    # orderNumber   The order number
    # type          sell or buy
    # rate          Price the order is selling or buying at
    # Amount        Quantity of order
    # total         Total value of order (price * quantity)
    def returnOpenOrders(self,currencyPair):
        return self.api_query('returnOpenOrders',{"currencyPair":currencyPair})

    # Returns your trade history for a given market, specified by the "currencyPair" POST parameter
    # Inputs:
    # currencyPair  The currency pair e.g. "BTC_XCP"
    # Outputs: 
    # date          Date in the form: "2014-02-19 03:44:59"
    # rate          Price the order is selling or buying at
    # amount        Quantity of order
    # total         Total value of order (price * quantity)
    # type          sell or buy
    def returnTradeHistory(self,currencyPair):
        return self.api_query('returnTradeHistory',{"currencyPair":currencyPair})

    def returnTradeHistory2(self,currencyPair,start,end):
        return self.api_query({"command":"returnTradeHistory",
                               "currencyPair":currencyPair,
                               "start":start,"end":end})

    def returnChartData(self,currencyPair,start,end,period):
        return self.api_query({"command":"returnChartData",
                               "currencyPair":currencyPair,
                               "start":start,"end":end,"period":period})

# Test returnTradeHistory2
#t1 = createTimeStamp('2017-01-01 00:00:00')
#t2 = createTimeStamp('2017-01-02 00:00:00')
#x = poloniex()
#a = x.returnTradeHistory2('USDT_BTC',t1,t2)
#print(a)