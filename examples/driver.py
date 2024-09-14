import importlib.util
import os
import json

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