# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 16:21:58 2019

@author: Hao
"""
import time
import dateparser
import pytz
import json
from datetime import datetime
from binance.client import Client
import urllib.request, json
def run(runfile):
  with open(runfile,"r") as rnf:
    exec(rnf.read())
with urllib.request.urlopen("https://www.binance.com/api/v1/ticker/allBookTickers") as url:
    data = json.loads(url.read().decode())    
symbol=[d['symbol'] for d in data if 'BTC' in d['symbol']]




 
