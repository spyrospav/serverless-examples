import time
IMPORT_START_TIME = time.time()
import numpy
from shapely.geometry import Point
IMPORT_END_TIME = time.time()
print(f"<import {IMPORT_END_TIME - IMPORT_START_TIME} seconds>")
def handler(event, context):
	patch = Point(0.0, 0.0).buffer(10.0)
	return patch.area

if __name__ == "__main__":
    area = handler(42, 42)
    print(area)