#!/usr/bin/env python
# coding: utf-8

import requests
import json
import time
import jprint
import RescueTimeActivity
import RescueTimeEfficiency
from datetime import date

While True:
	
	RescueTimeActivity("json", "2019-12-30")
	RescueTimeEfficiency("json", "2019-12-30")

	print(activity)
	print(efficiency)

	time.sleep(300)