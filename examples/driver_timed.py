import time
IMPORT_START_TIME = time.time()
import importlib.util
import os
import json
IMPORT_END_TIME = time.time()
print(f"<import {IMPORT_END_TIME - IMPORT_START_TIME} seconds>")
appname = os.environ['APPNAME']

modname = appname + '.lambda'

module = importlib.import_module(modname)

handler = module.handler

# open data.json file
with open(appname + '/data.json') as f:
    
    data = json.load(f)
    tests = data['tests']

    for entry in tests:
        event = entry['event']
        context = entry['context']
        print(handler(event, context))