import time
IMPORT_START_TIME = time.time()
import cv2
IMPORT_END_TIME = time.time()
print(f"<import {IMPORT_END_TIME - IMPORT_START_TIME} seconds>")
def lambda_handler(event, context):
	print("OpenCV installed version:" + cv2.__version__)
	return "It works!"

if __name__ == "__main__":
	lambda_handler(42, 42)