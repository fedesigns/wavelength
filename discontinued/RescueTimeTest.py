#!/usr/bin/env python
# coding: utf-8

# Installing libraries


import requests
import json
import time
import jprint
import RescueTimeActivity
import RescueTimeProductivity
from datetime import date

if __name__ == "__Main__":

    # Getting activity and productivity data in 5 min intervals (lowest possible resolution) in json format

    activity_parameters = {
        "format": "json",
        "pv": "interval",
        "rs": "minute",
        "rk": "activity",
        "rb": "2019-12-18",
        "re": "2019-12-24"
        
    }

    activity = requests.get("https://www.rescuetime.com/anapi/data?key=B63kQQhCfdXEaQLHbKVTt3x55woxyhk2kjabQ3BU", params = activity_parameters)
    print("Status code:")
    print(activity.status_code)



    def jprint(obj):
        # create a formatted string of the Python JSON object
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)


    jprint(activity.json())


    # #### Extracting activity outputs


    activity_log = activity.json()['rows']
    jprint(activity_log)


    # #### Extracting particular outputs with a loop



    categories = []

    for d in activity_log:
        category = d[4]
        categories.append(category)

    print(categories)


    # ### Getting productivity and efficiency data for each interval


    efficiency_parameters = {
        "format": "json",
        "pv": "interval",
        "rs": "minute",
        "rk": "efficiency",
        "rb": "2019-12-18",
        "re": "2019-12-24"
        
    }

    efficiency = requests.get("https://www.rescuetime.com/anapi/data?key=B63kQQhCfdXEaQLHbKVTt3x55woxyhk2kjabQ3BU", params = efficiency_parameters)
    print("Status code:")
    print(efficiency.status_code)




    jprint(efficiency.json())



    efficiency_log = efficiency.json()['rows']

    efficiencies = []

    for i in efficiency_log:
        efficiency = i[4]
        efficiencies.append(efficiency)

    print(efficiencies)






