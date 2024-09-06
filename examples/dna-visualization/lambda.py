import os
import sys
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from squiggle import transform
import requests

local_path = "./"

def visualize(data1, data2):
    
    return transform(data1) + transform(data2)

def handler(event, context=None):
    
    # Visualize sequences
    filename1 = os.path.join(local_path, event.get("filename1"))
    data1 = open(filename1, "r").read()
    filename2 = os.path.join(local_path, event.get("filename2"))
    data2 = open(filename2, "r").read()
    
    result = visualize(data1, data2)

    return result

if __name__ == "__main__":
    event = {
        "filename1": "gene1.txt",
        "filename2": "gene2.txt"
    }
    print(handler(event))