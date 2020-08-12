import pandas as pd
import numpy as np
class Algorithm:
    
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

A = Algorithm([1,1,1,1,1,1],[10,9,8,10,6,3],[[1],[2],[1],[2],[1],[2]])
A.start()
#цена падает - только лонг
#цена падает - только шорт
#цена растет - только шорт
#цена падает - лонг и шорт
#цена растет - лонг и шорт
#def Test(argument):
  #  output = [0]
  #  for i in range(1,len(arguments)):
      #  output.append()
