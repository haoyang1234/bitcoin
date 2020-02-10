# -*- coding: utf-8 -*-
"""
Created on Wed May  1 15:14:30 2019

@author: Hao
"""

import os
import json
import glob
import numpy as np
import pandas as pd
OpenT=[]
CloseT=[]
OpenP=[]
CloseP=[]
Return=[]
#result_folder = "C:\\Projects\\hao_sweetbytes\\Pumpdump&needlecatcher\\"
result_folder = "D:\\bitrepo\\Pumpdump&needlecatcher\\FebAplcsv\\"
file="ADABT.csv"
os.chdir(result_folder)
total_stats = pd.DataFrame()
for file in glob.glob('*.csv'):
 read_in_file = result_folder + file
 min_entries = pd.read_csv(read_in_file)
    
 buy_trades = min_entries.loc[min_entries.buy != 0, :]
 buy_trades_ind = list(buy_trades.index)
    
 sell_trades = min_entries.loc[min_entries.sell != 0, :]
 sell_trades_ind = list(sell_trades.index)

 comm_ind = (buy_trades_ind + sell_trades_ind)
 comm_ind.sort()
 entry=[]
 exitla=[]
 Op=[]
 Cp=[]
 all_trades = min_entries.loc[comm_ind, :]
 for i in range(0, int(all_trades.shape[0] / 2)):
     entry_ind = all_trades.index[i * 2] 
     exit_ind = all_trades.index[i * 2 + 1]
     entry_time = pd.to_datetime(all_trades.iloc[i * 2, 0])
     exit_time = pd.to_datetime(all_trades.iloc[i * 2 + 1, 0])
     p1=(all_trades.iloc[i * 2, 1])
     p2=(all_trades.iloc[i*2+1,1])
     entry.append(entry_time)
     exitla.append(exit_time)
     Op.append(p1)
     Cp.append(p2)
  
####### calculate average return
 Opp = pd.DataFrame(Op,columns=['Po'])
 Cpp = pd.DataFrame(Cp,columns=['Co'])
 data_div = Opp['Po']/Cpp['Co']
 data_div.mean(axis=0)
 OpenP.append(Op)
 CloseP.append(Cp)
 OpenT.append(entry)
 CloseT.append(exitla)
 Return.append(data_div)
 temp=pd.DataFrame(OpenT)
#######  see if time falls within specified frame.

    

