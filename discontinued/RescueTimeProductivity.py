#!/usr/bin/env python
# coding: utf-8

import requests
import json
import time
import jprint
import csv
from datetime import date

#global efficiency, efficiencies 


def RTProductivity(DataFormat, StartDate):

    #Setting parameters to request API data

    today = date.today()
    EndDate = today.strftime("%Y-%m-%d")

    efficiency_parameters = {
        "format": DataFormat,
        "pv": "interval",
        "rs": "minute",
        "rk": "efficiency",
        "rb": StartDate,
        "re": EndDate
    }

    efficiency = requests.get("https://www.rescuetime.com/anapi/data?key=B63kQQhCfdXEaQLHbKVTt3x55woxyhk2kjabQ3BU", params = efficiency_parameters)

    #print(efficiency)
    #print("Status code:")
    #print(efficiency.status_code)
    #return efficiency

    if DataFormat == "json":

        #jprint(efficiency.json())

        efficiency_log = efficiency.json()['rows']

        efficiencies = []

        for i in efficiency_log:
            logged_efficiency = i[4]
            efficiencies.append(logged_efficiency)

        print(efficiencies)

        return efficiency, efficiencies 
