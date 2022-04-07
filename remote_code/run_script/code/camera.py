import cv2
import imutils
import time
import numpy as np

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
class Camera(object):
	def __init__(self,):
		try:
			self.video = cv2.VideoCapture(0)
		except:
			self.video = cv2.VideoCapture(1)
		time.sleep(2.0)			
	def __del__(self):
		self.video.release()

	def get_frame(self):
		ret, frame = self.video.read()
		if ret:
			ret, jpeg = cv2.imencode('.jpg', frame, encode_param)
			return jpeg.tobytes()
