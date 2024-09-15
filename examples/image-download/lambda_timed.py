# -*- coding: utf-8 -*-
import time
IMPORT_START_TIME = time.time()
from skimage import io
import urllib.request
import skimage.segmentation as segmentation
IMPORT_END_TIME = time.time()
print(f"<import {IMPORT_END_TIME - IMPORT_START_TIME} seconds>")
def handler(event, context=None):
    url = event.get("url")
    urllib.request.urlretrieve(url, "./hi.jpg")
    img = io.imread('./hi.jpg')
    return img

if __name__ == "__main__":
    event = {
        "url": "https://upload.wikimedia.org/wikipedia/commons/3/38/JPEG_example_JPG_RIP_001.jpg"
    }
    print(handler(event))