# -*- coding: utf-8 -*-
from skimage import io
import urllib3
import skimage.segmentation as segmentation

def handler(event, context=None):
    url = event.get("url")
    # Create a PoolManager instance
    http = urllib3.PoolManager()
    
    # Make a GET request to the URL
    response = urllib3.request('GET', url)

    # Save the response data to a file
    filename = event.get("filename")
    with open(filename, 'wb') as f:
        f.write(response.data)

    img = io.imread(filename)
    return img

if __name__ == "__main__":
    event = {
        "url": "https://upload.wikimedia.org/wikipedia/commons/3/38/JPEG_example_JPG_RIP_001.jpg",
        "filename": "test.jpg"
    }
    print(handler(event))