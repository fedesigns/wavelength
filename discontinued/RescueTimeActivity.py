#!/usr/bin/env python
# coding: utf-8

import requests
import json
import time
import jprint
from datetime import date

#global activity, activities, categories


def RTActivity(DataFormat="json", StartDate="2019-12-31"):

    #Setting parameters to request API data

    today = date.today()
    EndDate = today.strftime("%Y-%m-%d")

    activity_parameters = {
        "format": DataFormat,
        "pv": "interval",
        "rs": "minute",
        "rk": "activity",
        "rb": StartDate,
        "re": EndDate
                        
    }

    activity = requests.get("https://www.rescuetime.com/anapi/data?key=B63kQQhCfdXEaQLHbKVTt3x55woxyhk2kjabQ3BU", params = activity_parameters)
    #print("Status code:")
    #print(activity.status_code)


    #jprint(activity.json())


    # Extracting activity outputs


    if DataFormat == "json":

        activity_log = activity.json()['rows']
        #jprint(activity_log)


        # Extracting particular outputs with a loop

        activities = []

        for d in activity_log:
            logged_activity = d[3]
            activities.append(logged_activity)

        categories = []

        for d in activity_log:
            category = d[4]
            categories.append(category)

        #print(categories)


        return activity, activities, categories
