import numpy
from shapely.geometry import Point

def handler(event, context):
	patch = Point(0.0, 0.0).buffer(10.0)
	return patch.area

if __name__ == "__main__":
    area = handler(42, 42)
    print(area)