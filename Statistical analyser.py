# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 12:15:16 2019
@author: Athan
"""
import json
import pandas as pd
import numpy as np
#from scipy.stats import percentileofscore
r=[]    
t=[]    
v=[]
l=[]
# import statsmodels.api as sm
#import/formating data 
#sourcefile =open("D:\\bitrepo\\Pumpdump&needlecatcher\\Dec-Feb\\Binance_AMBBTC.json")
sourcefile =open("C:\\Users\\Athan\\Desktop\\bitrepo\\Pumpdump&needlecatcher\\Feb-Apl\\Binance_VIBBTC.json")
#sourcefile =open("D:\\bitrepo\\Pumpdump&needlecatcher\\Feb-Apl\\Binance_ZRXBTC.json")
#sourcefile =open(read_in_file)
# sourcefile =open("C:\\Users\\Hao\\Desktop\\bitrepo\\Pumpdump&needlecatcher\\Binance_LUNBTC.json")
def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)
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
Vu=df["volume"].astype(float).values
temp=np.zeros(59)
#create moving average for prices
P60=running_mean(Pc,60)
P600=np.concatenate((temp,P60),axis=0)
P120=running_mean(Pc,120)
P1200=np.concatenate((temp,temp,P60),axis=0)
i=0
#create price divergence of MA vs Price. 
d60=Pc[59:]
d120=Pc[119:]/P120-1
d1200=np.concatenate((temp,temp,d120),axis=0)

#d60t=np.zeros(ldc) #Volume triggers
#120t=np.zeros(ldc) #number of trade triggers 

# while i<ldc:
  #  d60t[i]=np.percentile(d60[1+i:600+i], 99.9, axis=0) #volume trigger 
  #  d120t[i]=np.percentile(d120[1+i:600+i], 99.9, axis=0)
  #  i += 1
#calculate precentile of above mentioned divergence. 

times=df["Time"]
i=0
l=0
hour=120
ll=len(Po)-hour
R=[]
#Q=[]
L=[]
T=[]
V=[]
#Pc=[]
location=[]
#create a vector with smootthed volume data 
Vavg=np.mean(Vu)
#make a list of precentiles

#initiatng a magic target level
#create signals
i=0
while i<ll:
    # make the counting vector 
    prices=Po[i:i+hour]
    bb=np.ndarray.tolist(prices)
    a=max(bb)
    if a/Po[i]>1.10: #checking if criterion was met. 
        #record the max achievable price        
        prices1=Po[i:i+hour+120]
        avg60=P600[i:i+hour+120]
        avg120=P1200[i:i+hour+120]
        ad60=d600[i:i+hour+120]
        ad120=d1200[i:i+hour+120]
        tla=times[i]
        bb=np.ndarray.tolist(prices1)
        aa=max(bb)
        b = bb.index(aa)
        R.append(aa/Po[i])
        #record volume behavior
        volume=Vu[i:i+hour+120]
        L.append(b)
        #Record the price behavior within and after the pump period 
        #Q.append(prices1)
        #V.append(volume)
        V.append(avg60)    
        T.append(tla)     
        #skiiping ahead 3 hours 
        i+=hour+120
    i+=1    
     
#r.append(R)
#v.append(V)
#t.append(T)
#l.append(L)
#dfQ = pd.DataFrame(Q)
#dfQ = dfQ.transpose()
#dfV = pd.DataFrame(V)
#dfV = dfV.transpose()
#dfT = pd.DataFrame(T)
#dfL = pd.DataFrame(L)
#dfL = dfL.transpose()