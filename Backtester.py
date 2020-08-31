import pandas as pd
import numpy as np

def Segmentate(data, granule):
    
    time = pd.to_datetime(data["<TIME>"],format = "%H%M%S")
    new_dataFrame = ({'<TIME>':[],'<OPEN>':[],'<HIGH>':[],'<LOW>':[],'<CLOSE>':[],'<VOL>':[]})
   # print("a")
    i = 0
    td = pd.Timedelta(str(granule) + ' seconds')
    
   # print(td)
    while i < (len(data))-1:
        #begr = Time.clock()
        beg = i
        if time[beg].second%granule != 0:
            time[beg] = time[beg].replace(second = int(time[beg].second/granule)*granule)
        while i < (len(data))-1 and time[i+1]-time[beg] < td: #data["<TIME>"].iloc[i]==data["<TIME>"].iloc[i+1]:
            i+=1
        #print(Time.clock() - begr)
        end = i
        i+=1
        iterated = data.iloc[beg:end+1]
        new_dataFrame['<TIME>'].append(time[beg])
        new_dataFrame['<OPEN>'].append(iterated['<LAST>'].iloc[0])
        new_dataFrame['<CLOSE>'].append(iterated['<LAST>'].iloc[-1])
        new_dataFrame['<HIGH>'].append(np.max(iterated['<LAST>'].to_numpy()))
        new_dataFrame['<LOW>'].append(np.min(iterated['<LAST>'].to_numpy()))
        new_dataFrame['<VOL>'].append(sum(iterated['<VOL>'].to_numpy()))
        
    return pd.DataFrame(new_dataFrame)
    
class Algorithm:
    def __init__(self, timestamps, prices, features, capital = 100000, leverage = 1, fee = 0):
        self.timestamps = timestamps
        self.prices = prices
        self.features = features
        self.capital = capital
        self.allocated_capital = capital*leverage
        self.leverage = leverage
        self.returns = []
        self.sharpe = 0
        self.allocated_capital_log = [self.allocated_capital]
        self.max_drawdown = 0 
        self.positions = []
        self.iterator = 0
        self.len = len(prices)
        self.breakup = False
        self.transactions = []
        self.margins = [0]
        self.active_pos_iter= 0
        self.active_pos_iter_end = 0
        self.fee = fee
        self.flag = False
        if len(timestamps) != len(prices) or len(prices)!=len(features) or len(features)!=len(timestamps):
            self.breakup = True
            raise Exception("Inconsistent input")
    def logic(self, timestamp, price, features):
        pass       
    def start(self):
        if self.breakup == True:
            print("It's broken")
        else:
            marginsum = 0    
            while self.iterator < self.len:
                self.logic(self.timestamps[self.iterator],self.prices[self.iterator],self.features[self.iterator])
                quantity = sum([i["quantity"] for i in self.transactions[self.active_pos_iter:self.active_pos_iter_end]])
                self.margins.append(self.prices[self.iterator]*quantity)
                self.margins[-1]-=(sum([i["price"]*i["quantity"] for i in self.transactions[self.active_pos_iter:self.active_pos_iter_end]]))
                current_fee = self.fee*len(self.transactions)
                self.margins[-1]-=marginsum
                self.capital+=self.margins[-1]
                self.iterator += 1
                marginsum+=self.margins[-1] 
    def order(self, timestamp, price, quantity):
        self.transactions.append({"timestamp":timestamp,"price":price,"quantity":quantity})
        if self.transactions[-1]["quantity"]<0:
            self.transactions[-1]["price"]-=self.fee
        if self.transactions[-1]["quantity"]>0:
            self.transactions[-1]["price"]+=self.fee
        self.allocated_capital = abs(self.allocated_capital + price*quantity)
        if sum([i["quantity"] for i in self.transactions[self.active_pos_iter:]]) == 0:
            self.active_pose_iter = self.active_pos_iter_end
        self.active_pos_iter_end = len(self.transactions)
