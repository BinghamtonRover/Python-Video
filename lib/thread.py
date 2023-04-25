from network.generated import VideoCommand
import cv2
from multiprocessing import Process
from threading import Thread
import time

from network.generated import *
from network import VideoClient
import lib.constants as constants

cv2.setLogLevel(0)  # no logging from OpenCV

class CameraThread(Process):
	def __init__(self, camera_name, camera_id, client, framerate):
		print(f"[CameraThread] Initializing camera {camera_id}")
		self.camera_name = camera_name
		self.camera_id = camera_id
		self.client = client
		self.framerate = framerate
		self.is_active = False
		super().__init__()

	def can_read(self): 
		camera = cv2.VideoCapture(self.camera_id)
		if not camera.isOpened(): return False
		success, frame = camera.read()
		if not success: 
			print(f"[CameraThread.can_read] Camera {self.camera_id} is open but not responding")
		return success

	def run(self):
		camera = cv2.VideoCapture(self.camera_id)
		camera.set(cv2.CAP_PROP_FRAME_WIDTH, constants.default_resolution[0])
		camera.set(cv2.CAP_PROP_FRAME_HEIGHT, constants.default_resolution[1])
		try:
			self.is_active = True
			while True:
				success, frame = camera.read()
				if not success: 
					print(f"[CameraThread.run] Could not read frame for camera {self.camera_id}")
					return
				self.client.send_frame(self.camera_name, frame)
				time.sleep(self.framerate)
		except KeyboardInterrupt: pass

	def copy(self): 
		return CameraThread(camera_name=self.camera_name, camera_id=self.camera_id, client=self.client, framerate=self.framerate)

def get_threads(socket): 
	result = []
	cams = 0
	for index in range(10):
		thread = CameraThread(constants.camera_names[index], index, socket, framerate=constants.framerate)
		if thread.can_read(): result.append(thread)
	return result
