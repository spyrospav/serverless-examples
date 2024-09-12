import importlib
import os

appname = os.environ['APPNAME']

modname = appname + '.lambda'

module = importlib.import_module(appname)

handler = getattr(module, 'handler')

# open data.json file
with open(appname + '/data.json') as f:
    
    data = json.load(f)

    for entry in data:
        event = entry['event']
        context = entry['context']
        print(handler(event, context))