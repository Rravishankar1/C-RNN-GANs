import pandas as pd
import datetime as dt
import numpy as np
import random

class Loader(object):
    def __init__(self, datadir, select_validation_percentage, select_test_percentage):
        self.datadir = datadir
        self.pointer = {}
        self.pointer['validation'] = 0
        self.pointer['test'] = 0
        self.pointer['train'] = 0
        self.ticker_list = ['aapl', 'agq', 'cost', 'dis', 'gld', 'hyg', 'isrg', 'jnj', 'qqq', 'spy', 'vb', 'wmt']
        self.days_per_series = 60
        if not datadir is None:
            print ('Data loader: datadir: {}'.format(datadir))
            self.read_data(select_validation_percentage, select_test_percentage)

    def read_data(self, select_validation_percentage, select_test_percentage):
        self.data = {}
        self.data['validation'] = []
        self.data['test'] = []
        self.data['train'] = []
        
        self.dfs = {}
        for ticker in self.ticker_list:
            self.dfs[ticker] = pd.read_csv(f"{self.datadir}/{ticker}", index_col="Date", parse_dates=True)
        
        min_date = max([self.dfs[ticker].index[0] for ticker in self.ticker_list])
        max_date = min([self.dfs[ticker].index[-1] for ticker in self.ticker_list])
        for ticker in self.ticker_list:
            self.dfs[ticker] = self.dfs[ticker].loc[min_date:max_date]
        num_days = len(self.dfs[self.ticker_list[0]])
        # print(num_days)
        # print(min_date)
        # num_days = max_date - min_date
        # val_cutoff = min_date + (select_validation_percentage/100)*(num_days)
        # test_cutoff = min_date + (select_validation_percentage + select_test_percentage)/100*num_days
        val_cutoff = round(num_days*(1 - (select_test_percentage + select_validation_percentage)/100))
        test_cutoff = round(num_days*(1 - (select_test_percentage/100)))
        # print(val_cutoff, test_cutoff)
        
        for i in range(0, val_cutoff - self.days_per_series, self.days_per_series):
            self.data['train'].append(self.gen_series(i))
            # print(series)
            # self.data['train'].append(self.gen_series(date, date + pd.DateOffset(self.days_per_series)))
        for i in range(val_cutoff, test_cutoff - self.days_per_series, self.days_per_series):
            self.data['validation'].append(self.gen_series(i))
        for i in range(test_cutoff, num_days - self.days_per_series, self.days_per_series):
            self.data['test'].append(self.gen_series(i))
        # print(self.data['train'])
            
    def gen_series(self, i):
        series = np.ndarray(shape=(self.days_per_series, 5*len(self.ticker_list)))
        days = self.dfs[self.ticker_list[0]].index[i:i+self.days_per_series]
        for j, ticker in enumerate(self.ticker_list):
            # print(j, ticker)
            # print(self.dfs[ticker][['Open', 'Close', 'High', 'Low', 'Volume']].iloc[i:i+self.days_per_series])
            series[:, 5*j : 5*j + 5] = self.dfs[ticker][['Open', 'Close', 'High', 'Low', 'Volume']].iloc[i:i+self.days_per_series]
            assert(pd.Index.equals(days, self.dfs[ticker].index[i:i+self.days_per_series]))
        return series

    def get_batch(self, batchsize, part='train'):
        return random.choices(self.data[part], k=batchsize)

    def get_num_features(self):
        return 5*len(self.ticker_list)