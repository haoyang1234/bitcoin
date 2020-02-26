# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 22:54:48 2019
@author: Hao
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#import statsmodels.api as sm
#import/formating data 
#sourcefile =open("C:\\Users\\Athan\\Desktop\\bitrepo\\Pumpdump&needlecatcher\\Binance_BlZBTC.json")
sourcefile =open(read_in_file)
#sourcefile =open("C:\\Projects\\hao_sweetbytes\\Pumpdump&needlecatcher\\Binance_LUNBTC.json")
data=json.load(sourcefile)
#json.dumps(data)
df = pd.DataFrame(data,columns=['Time', 'open', 'high', 'low', 'close', 'volume', 'ctime', 'quotevolume', 'Ntrades', 'takerbuybaseassetvolume', 'takerbuyquotevolume', 'dN'])
df['Time']=pd.to_datetime(df['Time']/1000, unit='s')
def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)
#preproessing data
V=df["volume"].astype(float).values
N=df["Ntrades"].astype(float).values 
Po=df["open"].astype(float).values  
Pc=df["close"].astype(float).values
Ph=df["high"].astype(float).values
Pl=df["low"].astype(float).values
Vask=df["takerbuybaseassetvolume"].astype(float).values
Ntrades=df["Ntrades"].astype(float).values
Vbid=V-Vask
dV=np.diff(V)
dPo=np.diff(np.log(Po))
dPoc=np.log(Pc)-np.log(Po)
ma=60 #magic number for moving average, as the stoplOss level
aa=20
c=int(aa/2)
pre=10080 #magic number for initiation period 
Npre=10080 #magicc number for Number of traders initiation period and rolling forward average 
V30=running_mean(V,aa)
N30=running_mean(N,aa)
Po90=running_mean(Po,ma)
Ntrades=running_mean(N,aa)
# 1231243125445 
Po30=running_mean(Po,aa)
# prefil an dataframe 
Var2 = np.vstack((Po[c-1+ma+pre:],Po30[pre+ma-c:],Po90[pre+c:],dPoc[c-1+ma+pre:], V[c-1+ma+pre:],V30[ma-c+pre:],N[c-1+ma+pre:],N30[ma-c+pre:])). T  
df2 = pd.DataFrame(Var2,index=df['Time'][c-1+ma+pre:],columns=['P','P30','P90','dPoc','V','V30','N','N30'])
ll=len(df2.index)
#signal1=np.zeros(ll) #collum for entry signal volume signal 
#signal2=np.zeros(ll) #moving average signal  
signal3=np.zeros(1) #confirmation signal
#signal4=np.zeros(ll) #number of trades signal
signal5=np.zeros(1) #confirmation singal #2
buytheo=np.zeros(ll)  #artificial theoratical price for buying
selltheo=np.zeros(ll)  #artificial theoratical price for selling
buy=np.zeros(ll) #buy
sell=np.zeros(ll) #sell
asset=np.zeros(ll) #initial investment amount
asset[0]=0
position=np.zeros(ll) #position
pnl=np.zeros(ll) #PNL
fees=np.zeros(ll) #fees
vtrigger=np.zeros(ll) #Volume triggers
ntrigger=np.zeros(ll) #number of trade triggers 
#buying interest triggers 
pnl=np.zeros(ll)
fees=np.zeros(ll) #pnl
i = 0
target=0 #initiating a magic target level
#create signals
while i<ll:
    vtrigger[i]=np.percentile(V30[1+i:pre+i], 99.9, axis=0) #volume trigger 
    ntrigger[i]=np.percentile(N30[pre-Npre+1+i:pre+i], 99.9, axis=0) #number of trades trigger
    i += 1
    
signal1=((df2["V"]>vtrigger).values)*1 #volume trigger 
signal4=((df2["N"]>ntrigger).values)*1  #number of trades trigger
signal2=((df2["P"]>df2["P30"]).values)*1  #moving average cross over
signal3=np.append(signal3,signal1[:-1]) #lagged signal trigger -1
signal5=np.append(signal5,signal3[:-1]) #lagged signal trigger -2
signal6=((df2["dPoc"]>0).values)*1#in minute momentum detection 
buytheo=2*df2["P"]-df2["P30"]
selltheo=2*df2["P"]-df2["P90"]

combo=signal1*signal2*signal4*signal6#*signal5*signal3
spread=selltheo-df2["P"]

#generate entry signals
spread=selltheo-df2["P"]
i = 1
b=0.00
avg=0.00
buysum=0
while i<ll:
    if combo[i-1]==1 and position[i-1]==0 and buysum==0 :  # and df2["V30"][i-1]>df2["V30"][i-2]
        b=min(df2["V"][i-1]*0.05*df2["P"][i],10) #assuming buying only 25% of all avialable volume or a max of 10, for risk reasons. 
        buy[i]=b
        fees[i]=buy[i]*df2["P"][i]*0.00075
        target=selltheo[i]
        pnl[i]=pnl[i]-fees[i]
    if i>=10:
        avg=(sum(signal1[i-10:i])+sum(signal2[i-10:i]))/(20)
        buysum=sum(buy[i-120:i])
    if spread[i]<0 and position[i-1]!=0 and signal1[i-1] *signal2[i-1]==0 and avg<=0.5 or df2["P"][i]>=target:
        sell[i]=position[i-1]     
    position[i]=position[i-1]+buy[i]/df2["P"][i]-sell[i]
    if sell[i]!=0:
        fees[i]=sell[i]*df2["P"][i]*0.00075
        pnl[i]=sell[i]*df2["P"][i]-fees[i]-b
    i += 1
a=np.sum(pnl)
print(a)
Var3 = np.vstack ((signal1,signal2,signal4,signal6,buytheo,selltheo,buy,sell,asset,position,pnl,fees)). T 
df3=pd.DataFrame(Var3,index=df['Time'][c-1+ma+pre:],columns=['signal1','signal2','signal4','signal6','buytheo','selltheo','buy','sell','asset','position','pnl','fees'])
df2=df2.join(df3)
#df2.to_csv(write_in_file)
#define a buying strategy with 10 BTC under management

#filtering out big numbers
#construct a preliminary rule
#test the result 

#plt.subplot(4,1,1)
#plt.plot(V30)

#plt.subplot(4, 1, 2)
#plt.plot(V)
#plt.subplot(4,1,3)

#plt.plot(Po)
#plt.subplot(4,1,4)
#plt.plot(Ntrades)


