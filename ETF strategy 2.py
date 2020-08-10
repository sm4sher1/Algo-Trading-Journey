import re
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr


yf.pdr_override()
#activates a yahoo finance workaround
now = dt.datetime.now()
#today
start = dt.datetime(2018,1,1)
#the start of the backtest
etfs = ['FDN','IBB','IEZ','IGV','IHE','IHF','IHI','ITA','ITB','IYJ','IYT','IYW','IYZ'
        ,'KBE','KCE','KIE','PBJ','PBS','SMH','VNQ','XLB','XLP','XLU','XOP','XRT','GLD'
        ,'IWF','TLT','SHY','EEM','SQQQ','SPDN','PSQ','SH']
#all of the different ETF's that will be traded on
monthly_return = []      
#Will track the return
df = pdr.get_data_yahoo(etfs, start, now)
#gets the data for all the etfs, I think it is required for the for loop/

pos = 0
num = 0
percentchange = []
positions = []
#to track open positions
open_price = []
#to track the price when you open a posiiton
counter = 0
for i in df.index: 
    #iterates through every day from the start to today
    for etf in etfs:
        #goes through every etf per day to determine whether or not it is a buying opurtiunity 
        etf_df = pdr.get_data_yahoo(etf, start, now)
       #gets the specific etf data
        emasUsed = [3,5,8,10,12,15,30,35,40,45,50,60]
        #sets the emas
        close = etf_df["Adj Close"][i]
        #calculates the closing price of the stock
        for x in emasUsed:
            ema = x
            etf_df["Ema_"+str(ema)]=round(etf_df.iloc[:,4].ewm(span=ema, adjust=False).mean(),2)
            #calculates the ema of the etf
        cmin = min(etf_df["Ema_3"][i],etf_df["Ema_5"][i],etf_df["Ema_8"][i],etf_df["Ema_10"][i],etf_df["Ema_12"][i])
        #short term emas
        cmax = max(etf_df["Ema_30"][i],etf_df["Ema_35"][i],etf_df["Ema_40"][i],etf_df["Ema_45"][i],etf_df["Ema_50"][i],etf_df["Ema_60"][i])
        #long term ema - if cmin breaks through cmax, it is in an uptrend
        if(cmin > cmax):
            print("Up-trend: "+etf)
            if(pos<=10 and etf not in positions):
                        #if there are less then 10 positions and  position with this etf is not already open, buy.
                bp = close
                #the buy price == the close price of that day
                pos += 1
                #positions + 1
                print("Buying ",etf," at: "+str(bp))
                positions.append(etf)
                #adds the bought etf to the list tracking open positions
                open_price.append(bp)                
                #appends the buy price onto the list, so you can find the profit.
        elif(cmin < cmax):
            print("Down-trend :"+etf)
            if etf in positions:
                for t_etf in positions:
                       #if it is in a down tend and there is a position open
                    if t_etf == etf:
                        positions.remove(t_etf)
                        #remove the etf from the list of positions
                    counter = -1
                    counter += 1
                        #find the buy price as it is in the same position as the etf was.
                print(positions)
                print(open_price)
                bp = open_price[counter]
                bp = int(bp)
                #find the buy price
                open_price.pop(counter)
                #remove the buy price from the list
                counter = -1
                #reset the counter
                pos -= 1
                #remove one from the positions
                sp = close
                print("Selling ",etf," at: "+str(sp))
                pc = (sp/bp-1)*100
                #calculate the percentage change
                percentchange.append(pc)
                #append it to the percentage change list

print(percentchange)          
