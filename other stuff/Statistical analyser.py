# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 12:15:16 2019
@author: Athan
"""
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
# import statsmodels.api as sm
#import/formating data 
sourcefile =open("F:\Bitcoins\\Binance_IOTXBTC.json")
# sourcefile =open("C:\\Users\\Hao\\Desktop\\bitrepo\\Pumpdump&needlecatcher\\Binance_LUNBTC.json")
# filter price surges 
data=json.load(sourcefile)
#json.dumps(data)
df = pd.DataFrame(data,columns=['Time', 'open', 'high', 'low', 'close', 'volume', 'ctime', 'quotevolume', 'Ntrades', 'takerbuybaseassetvolume', 'takerbuyquotevolume', 'dN'])
df['Time']=pd.to_datetime(df['Time']/1000, unit='s')
#filter out 
Po=df["open"].astype(float).values  
Pc=df["close"].astype(float).values
Ph=df["high"].astype(float).values
Pl=df["low"].astype(float).values
i=0
l=0
hour=240
ll=len(Po)-hour
Rmax=[]
P=[]
Q=[]
location=[]
# i = 0
#initiating a magic target level
#create signals
while i<ll:
    # make the counting vector 
    periods=Po[i:i+hour]
    bb=np.ndarray.tolist(periods)
    a=max(bb)
    b = bb.index(a)
    if a/Po[i]>1.10: #checking if criterion was met. 
        #record the max achievable price
        Rmax.append(a/Po[i])
        periods1=Po[i:i+hour+120]
        #record the location of the max price
        location.append(b)
        #Record the price behavior within the pump period 
        P.append(periods)
        Q.append(periods1)
        l+=1
        #skiiping ahead 3 hours 
        i+=hour
    i+=1