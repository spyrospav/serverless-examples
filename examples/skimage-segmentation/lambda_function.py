# -*- coding: utf-8 -*-
import time
IMPORT_START_TIME = time.time()
from skimage import io
import urllib.request
import skimage.segmentation as segmentation
IMPORT_END_TIME = time.time()
print(f"<import {IMPORT_END_TIME - IMPORT_START_TIME} seconds>")
def handler(event, context=None):
    sleep_time = event.get("sleep_time", 0)
    time.sleep(sleep_time)
    event = {
        "url": "https://upload.wikimedia.org/wikipedia/commons/3/38/JPEG_example_JPG_RIP_001.jpg"
    }
    url = event.get("url")
    urllib.request.urlretrieve(url, "/tmp/hi.jpg")
    img = io.imread('/tmp/hi.jpg')
    print(img)
    return {"import_time": IMPORT_END_TIME - IMPORT_START_TIME}
