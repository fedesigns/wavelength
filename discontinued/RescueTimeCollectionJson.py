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


#def RTCollection():

    

while True:

    #RTCollection()
    #global activity, efficiency

    #activity, activities, categories = RTActivity("json", "2020-01-06")
    efficiency, efficiencies = RTProductivity("json", "2020-1-6")

    #jp(activity.json())
    #jp(efficiency.json())
    print(efficiencies)

    time.sleep(300)

    #schedule.every().minute.at(":01").do(RTCollection)