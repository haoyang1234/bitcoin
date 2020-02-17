# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 23:32:45 2019

@author: Hao
"""
#aggregate 

import numpy as np
import pandas as pd
import os
import glob
import json
r=[]    
t=[]    
v=[]
l=[]
q=[]
aa60=[]
aa120=[]
dd60=[]
dd120=[]
#read_folder = "C:\\Users\\Athan\\Desktop\\bitrepo\\Pumpdump&needlecatcher\\Feb-Apl\\"
read_folder = "D:\\bitrepo\\Pumpdump&needlecatcher\\Feb-Apl\\"
os.chdir(read_folder)
total_stats = pd.DataFrame()
def run(runfile):
  with open(runfile,"r") as rnf:
    exec(rnf.read())
def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)

for file in glob.glob('*.json'):
    read_in_file = read_folder + file
    pair_name = file[8:13]
    print(pair_name)
    sourcefile =open(read_in_file)
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
    times=df["Time"]
    i=0
    hour=120
    ll=len(Po)-hour
    R=[]
    Q=[]
    L=[]
    T=[]
    V=[]
    A60=[]
    A120=[]
    D60=[]
    D120=[]
#Pc=[]
    location=[]
# create a vector with smootthed volume data 
    temp=np.zeros(59)
#create moving average for prices
    P60=running_mean(Pc,60)
    P600=np.concatenate((temp,P60),axis=0)
    P120=running_mean(Pc,120)
    P1200=np.concatenate((temp,temp,P60),axis=0)
    i=0
#create price divergence of MA vs Price. 
    d60=Pc[59:]/P60-1
    d600=np.concatenate((temp,d60),axis=0)
    d120=Pc[119:]/P120-1
    d1200=np.concatenate((temp,temp,d120),axis=0)
    Vavg=np.mean(Vu)
#make a list of precentiles 
#initiating a magic target level
#create signals
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
        vp=np.mean(Vu[i:i+hour+120])/Vavg
        bb=np.ndarray.tolist(prices1)
        aa=max(bb)
        b = bb.index(aa)
        R.append(aa/Po[i])
        #record volume behavior
        volume=Vu[i:i+hour+120]
        L.append(b)
        #Record the price behavior within and after the pump period 
        Q.append(prices1)
        #V.append(volume)
        T.append(tla)
        V.append(vp)
        A60.append(avg60)
        A120.append(avg120)
        D60.append(ad60)
        D120.append(ad120)
        #skiiping ahead 3 hours 
        i+=hour+120
     i+=1
    r.append(R)
    v.append(V)
    t.append(T)
    l.extend(L)
    q.extend(Q)
    aa60.extend(A60)
    aa120.extend(A120)
    dd60.extend(D60)
    dd120.extend(D120)

dfD60 = pd.DataFrame(dd60).iloc[0:1]
dfD120 = pd.DataFrame(dd120)
dfP60 = pd.DataFrame(aa60)
dfP120 = pd.DataFrame(aa120)
dfQ = pd.DataFrame(q)

#testing performance results How to 1-0-1
# record location first time when the ratio d moves above 4%
temp=dfD60[dfD60 >=0.039].bfill(axis=1).iloc[:, 0]
location=[]
xx=len(dfD60)
x=0
pprice=[]
mprice=[]
while x<=xx-1:
    try:
     cla=dfD60.iloc[x][dfD60.iloc[x] == temp[x]].index[0]
     location.append(cla)
     pprice.append(q[x][cla])
     mprice.append(q[x][l[x]])
     x+=1
    except IndexError:
     location.append(0)
     pprice.append(q[x][cla])
     mprice.append(q[x][l[x]]) 
     x+=1
     
# record the location of max price
# compare the absolute price at 4% and max