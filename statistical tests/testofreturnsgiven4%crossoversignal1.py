# -*- coding: utf-8 -*-
"""
Created on Mon May 20 11:04:56 2019

@author: Athan
"""
import numpy as np
import pandas as pd
import os
import glob
import json
avg=[]
total=[]
pricelist=[]
counter1=list(range(1))
counter2=list(range(1))

#read_folder = "C:\\Users\\Athan\\Desktop\\bitrepo\\Pumpdump&needlecatcher\\Feb-Apl\\"
read_folder = "D:\\bitrepo\\Pumpdump&needlecatcher\\testrun\\"
os.chdir(read_folder)
total_stats = pd.DataFrame()
def run(runfile):
  with open(runfile,"r") as rnf:
    exec(rnf.read())
def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)
shortPavg=7
longPavg=30
shortVavg=30
longVavg=60
hour=60
shortPappend=np.zeros(shortPavg-1)
longPappend=np.zeros(longPavg-1)
shortVappend=np.zeros(shortVavg-1)
longVappend=np.zeros(longVavg-1)
#preset winners
Wprices=[]
Wptrigger=[]
Wvtrigger=[]
Wv=[]
Wpdivergence=[]
Wvdivergence=[]
#preset losers 
Lprices=[]
Lptrigger=[]
Lvtrigger=[]
Lv=[]
Lpdivergence=[]
Lvdivergence=[]
for x in counter1:
        for y in counter2:
            r=[]
            for file in glob.glob('*.json'):
             R=[]
             read_in_file = read_folder + file
             pair_name = file[8:13]
             print(pair_name)
             sourcefile =open(read_in_file)
             data=json.load(sourcefile)
             
             df = pd.DataFrame(data,columns=['Time', 'open', 'high', 'low', 'close', 'volume', 'ctime', 'quotevolume', 'Ntrades', 'takerbuybaseassetvolume', 'takerbuyquotevolume', 'dN'])
             Pc=df["close"].astype(float).values
             V=df["volume"].astype(float).values
             ll=len(Pc)-hour
             ptrigger=np.zeros(ll+hour)
             vtrigger=np.zeros(ll+hour)
             #Pc=[]
             # create a vector with smootthed volume data 
             #create moving average for prices
             temp=running_mean(Pc,shortPavg)
             Pshort=np.concatenate((shortPappend,temp),axis=0)
             #temp=running_mean(Pc,longPavg)
             #Plong=np.concatenate((longPappend,temp),axis=0)
             temp=running_mean(V,shortVavg)
             Vshort=np.concatenate((shortVappend,temp),axis=0)
             temp=running_mean(V,longVavg)
             Vlong=np.concatenate((longVappend,temp),axis=0)
              #create price divergence of MA vs Price. 
             Pdivergence=Pc/Pshort-1
             Vdivergence=Vshort/Vlong-1
             a=0
             while a<ll+hour:
                 try:
                     vtrigger[a]=np.percentile(Vdivergence[a-240:a], 99.9, axis=0)
                     ptrigger[a]=np.percentile(Pdivergence[a-240:a], 99.0, axis=0)
                     a+=1
                 except:
                     a+=1
             selltrigger=np.concatenate((np.zeros(1),vtrigger[1:]-vtrigger[:-1]),axis=0) #which is the first order derivative of vtrigger
              #vtrigger[i]=np.percentile(V30[1+i:pre+i], 99.9, axis=0) #volume trigger 
              #ntrigger[i]=np.percentile(N30[pre-Npre+1+i:pre+i], 99.9, axis=0) #number of trades trigger
              #i += 1
             #check the stats of winning trade
             #check the stats of losing trade
             #given criterions
             #stats to check, what's going on with volume? 
             #what's prices action?
             i=0
             while i<ll:
                 # make the counting vector     
                 if Pdivergence[i]>=ptrigger[i] and ptrigger[i]!=0:#SLPdivergence[i]>0.051+x*0.001: #checking if price criterion was met                      
                   if Vdivergence[i]>=vtrigger[i]: #checking if volume criterion was met.
                       try:
                           Aprices=Pc[i:i+hour*3] #record price
                           Aptrigger=ptrigger[i:i+hour*3] #record ptriggers
                           Avtrigger=vtrigger[i:i+hour*3] #record vtriggers 
                           Av=V[i:i+hour*3] #record volume
                           Apdivergence=Pdivergence[i:i+hour*3]
                           Avdivergence=Vdivergence[i:i+hour*3]
                           targetprice=Aprices[30]
                           R.append(targetprice/Pc[i])
                           #distiguishing winner vs loser
                           if targetprice/Pc[i]>1:
                               Wprices.append(Aprices)
                               Wv.append(Av)
                               Wpdivergence.append(Apdivergence)
                               Wvdivergence.append(Avdivergence)
                               Wptrigger.append(Aptrigger)
                               Wvtrigger.append(Avtrigger)
                           else:
                                Lprices.append(Aprices)
                                Lv.append(Av)
                                Lpdivergence.append(Apdivergence)
                                Lvdivergence.append(Avdivergence)
                                Lptrigger.append(Aptrigger)
                                Lvtrigger.append(Avtrigger)
                               
                           #dfMv=pd.DataFrame(AMavg)
                     #finding the location where quickmovingaverage moves below longmoving average for the first time
                           #temp=dfMv[dfMv <=0.001].bfill(axis=0).iloc[:, 0]
                           #location=dfMv.loc[dfMv[0] == temp[0]].index[0]
                     #record target selling price.                  
                           #targetprice=Aprices1[location]
                           #R.append(targetprice/Pc[i])
                     #skiiping ahead 4 hours 
                           i+=hour
                       except:
                            i+=1                    
                    #record the max achievable price        
                 i+=1
             r.extend(R)

            average=sum(r)/len(r)
            tot=sum(r)
            avg.append(average)
            total.append(tot)
