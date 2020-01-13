#!/usr/bin/env python
# coding: utf-8

import requests
import json
import time
from jprint import jp
import RescueTimeActivity
import RescueTimeProductivity
from RescueTimeActivity import RTActivity
from RescueTimeProductivity import RTProductivity
from datetime import date
import schedule
import numpy as np
from pandas import read_csv


#data = np.array([5], [])
data = read_csv("https://www.rescuetime.com/anapi/data?key=B63kQQhCfdXEaQLHbKVTt3x55woxyhk2kjabQ3BU&format=csv&pv=interval&rs=minute&rk=efficiency&rb=2020-01-06&re=2020-02-05")

print(data)

'''    

while True:

    #RTCollection()
    #global activity, efficiency

#    activity, activities, categories = RTActivity("json", "2019-12-29")

    jp(activity.json())
    jp(efficiency.json())

    time.sleep(60)

    #schedule.every().minute.at(":01").do(RTCollection)
'''