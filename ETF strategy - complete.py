import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr


yf.pdr_override()
now = dt.datetime.now()
start = dt.datetime(2019,8,1)
etfs = ['FDN','IBB','IEZ','IGV','IHE','IHF','IHI','ITA','ITB','IYJ','IYT','IYW','IYZ'
        ,'KBE','KCE','KIE','PBJ','PBS','SMH','VNQ','XLB','XLP','XLU','XOP','XRT','GLD'
        ,'IWF','TLT','SHY','EEM','SQQQ','SPDN','PSQ','SH']
df = pdr.get_data_yahoo(etfs, start, now)
profit = 0
pos = 0
num = 0
percentchange = []
positions = []
open_price = []
counter = 0
trades = 0

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
            if(pos<15 and etf not in positions):
                bp = close
                pos += 1
                print("Buying ",etf," at: "+str(bp))
                positions.append(etf)
                open_price.append(bp)                
        elif(cmin < cmax):
            print("Down-trend :"+etf )
            if etf in positions:
                for t_etf in positions:
                    if t_etf == etf:
                        positions.remove(t_etf)
                    counter = -1
                    counter += 1
                bp = open_price[counter]
                bp = int(bp)
                if((bp * 1.075) <= close): #12 months 830 profit - 11 trades/11 months 80 profit 107 trades(if cmin <cmax i think)
                    open_price.pop(counter)
                    print(positions)
                    print(open_price)
                    counter = -1
                    pos -= 1
                    sp = close
                    earning = sp - bp
                    profit += earning
                    print("Selling ",etf," at: "+str(sp))
                    pc = (sp/bp-1)*100
                    percentchange.append(pc)
                    trades += 1
                elif((bp * 0.95) <= close):
                    open_price.pop(counter)
                    print(positions)
                    print(open_price)
                    counter = -1
                    pos -= 1
                    sp = close
                    earning = sp - bp
                    profit += earning
                    print("Selling ",etf," at: "+str(sp))
                    pc = (sp/bp-1)*100
                    percentchange.append(pc)
                    trades += 1
        print(i)
    print("Profit: ",profit)
    print(percentchange)          
print("Profit: ",profit)
print(positions)
