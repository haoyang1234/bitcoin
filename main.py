# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 19:58:45 2019

@author: Hao
"""

import numpy as np
import pandas as pd
import os
import glob
import json

read_folder = "F:\\Bitcoins\\"
write_folder="F:\\Bitcoins\\FebAplcsv\\"
os.chdir(read_folder)
total_stats = pd.DataFrame()
def run(runfile):
  with open(runfile,"r") as rnf:
    exec(rnf.read())
for file in glob.glob('*.json'):
    read_in_file = read_folder + file
    pair_name = file[9:-5]
    print(pair_name)
    add=".csv"
    write_name=pair_name+add
    w=write_folder+write_name
    run("pump detector.py")
    
