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

    

CollectionStatus = "on"

while CollectionStatus == "on":

    #RTCollection()
    #global activity, efficiency

    activity, activities, categories = RTActivity("json", "2019-12-29")
    efficiency, efficiencies = RTProductivity("json", "2019-12-29")

    jp(activity.json())
    jp(efficiency.json())

    time.sleep(60)

    #schedule.every().minute.at(":01").do(RTCollection)