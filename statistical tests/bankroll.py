# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 14:13:51 2019

@author: Hao
"""

import os
import json
import glob
import numpy as np
import pandas as pd
total_pnl = []
name = []
folder1 = "C:\\Users\\Hao\\Desktop\\bitrepo\\Pumpdump&needlecatcher\\Pc-Po 99.5\\"
folder2 = "D:\\bitrepo\\Pumpdump&needlecatcher\\FebAplcsv\\"
result_folder = folder2  # CHANGE THIS TO ADJUST IT TO YOUR FOLDER
os.chdir(result_folder)
for file in glob.glob('*.csv'):
    read_in_file = result_folder + file
    pair_name = file
    print(pair_name)
    a = pd.read_csv(read_in_file)  # reading CSV
    pnl = a['pnl'].tolist()
    total_pnl.append(pnl)
    name.append(pair_name[:-4])
data_transposed = zip(total_pnl)
df = pd.DataFrame(total_pnl)
df = df.transpose()
total_sum = df.sum(axis=1, skipna=True)
a = total_sum[1372:]
N = 1440
daily = a.groupby(a.index // N).sum()
print('done')
