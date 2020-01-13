#!/usr/bin/env python
# coding: utf-8

import json
from jprint import jp
   
with open("/Users/fedetiersen/OneDrive - Imperial College London/DE4/Sensing & IOT/Project/wavelenght/muse-test-json.json", "r") as read_file:

    data = json.load(read_file)#, sort_keys=True, indent=4)

jp(data)