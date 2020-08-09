import re
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr


yf.pdr_override()
now = dt.datetime.now()
start = dt.datetime(2018,1,1)
etfs = ['FDN','IBB','IEZ','IGV','IHE','IHF','IHI','ITA','ITB','IYJ','IYT','IYW','IYZ'
        ,'KBE','KCE','KIE','PBJ','PBS','SMH','VNQ','XLB','XLP','XLU','XOP','XRT','GLD'
        ,'IWF','TLT','SHY','EEM','SQQQ','SPDN','PSQ','SH']
monthly_return = []      
df = pdr.get_data_yahoo(etfs, start, now)

pos = 0
num = 0
percentchange = []
positions = []
open_price = []
counter = 0
for i in df.index: 
    for etf in etfs:
        etf_df = pdr.get_data_yahoo(etf, start, now)
        emasUsed = [3,5,8,10,12,15,30,35,40,45,50,60]
        close = etf_df["Adj Close"][i]
        for x in emasUsed:
            ema = x
            etf_df["Ema_"+str(ema)]=round(etf_df.iloc[:,4].ewm(span=ema, adjust=False).mean(),2)
        cmin = min(etf_df["Ema_3"][i],etf_df["Ema_5"][i],etf_df["Ema_8"][i],etf_df["Ema_10"][i],etf_df["Ema_12"][i])
        cmax = max(etf_df["Ema_30"][i],etf_df["Ema_35"][i],etf_df["Ema_40"][i],etf_df["Ema_45"][i],etf_df["Ema_50"][i],etf_df["Ema_60"][i])
        if(cmin > cmax):
            print("Up-trend: "+etf)
            if(pos<=10 and etf not in positions):
                bp = close
                pos += 1
                print("Buying ",etf," at: "+str(bp))
                positions.append(etf)
                open_price.append(bp)                
        elif(cmin < cmax):
            print("Down-trend :"+etf)
            if etf in positions:
                for t_etf in positions:
                    if t_etf == etf:
                        positions.remove(t_etf)
                    counter = -1
                    counter += 1
                print(positions)
                print(open_price)
                bp = open_price[counter]
                bp = int(bp)
                open_price.pop(counter)
                counter = -1
                pos -= 1
                sp = close
                print("Selling ",etf," at: "+str(sp))
                pc = (sp/bp-1)*100
                percentchange.append(pc)

print(percentchange)          
