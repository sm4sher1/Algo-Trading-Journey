import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr


yf.pdr_override()
now = dt.datetime.now()
start = dt.datetime(2018,1,1)
emasUsed = [60] 
etfs = ['FDN','IBB','IEZ','IGV','IHE','IHF','IHI','ITA','ITB','IYJ','IYT','IYW','IYZ'
        ,'KBE','KCE','KIE','PBJ','PBS','SMH','VNQ','XLB','XLP','XLU','XOP','XRT']
monthly_return = []
top_etfs = [None,None,None,None,None,None]
total = 0

##for etf in etfs:
##    df = pdr.get_data_yahoo(etf, start, now)
##    monthly_returns = df['Adj Close'].resample('M').ffill().pct_change()      
##    #print("ETF: ",etf," Monthly Returns: ",monthly_returns)
##    monthly_return.append(str(monthly_returns))
##    for i in range(30):
##        daily_returns = df['Adj Close'].resample('D').ffill().pct_change()
##        cumulative_returns = (daily_returns + 1).comprod()
##        print(cumulative_returns)
        

df = pdr.get_data_yahoo(etfs, start, now)
daily_return = (df['Adj Close'].pct_change())
monthly_return = (df['Adj Close'].resample('M').ffill().pct_change())
print(monthly_return)
print(daily_return)

for i in df.index:
    #print(daily_return['FDN'])
    if daily_return['FDN'][i] > daily_return['IBB'][i]:
        print("FDN is better than IBB")
    else:
        print("IBB is better than FDN")

    




    
