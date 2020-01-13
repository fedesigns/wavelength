#!/usr/bin/env python
# coding: utf-8
import json

def jp(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)