from multiprocessing import Process, Queue
from threading import Thread

import cv2
import time

from network.generated import *
import lib.constants as constants

cv2.setLogLevel(0)  # no logging from OpenCV

class CameraThread(Process):
	def __init__(self, camera_id, details, client, queue):
		print(f"[CameraThread] Initializing camera {camera_id}")
		self.queue = queue
		self.camera_id = camera_id
		self.set_status(CameraStatus.CAMERA_LOADING)
		self.details = details.SerializeToString()
		self.client = client
		self.check_camera()
		super().__init__()

	def set_status(self, status): 
		"""Sets the status for this camera.

		This is needed because the server is running in a whole different process entirely, and setting
		self.status won't be reflected in the server's process. The Queue works across processes.
		"""
		self.queue.put([self.camera_id, status])

	def check_camera(self): 
		camera = cv2.VideoCapture(self.camera_id)
		if not camera.isOpened(): 
			self.set_status(CameraStatus.CAMERA_DISCONNECTED)
		else: 
			success, frame = camera.read()
			if not success: 
				self.set_status(CameraStatus.CAMERA_NOT_RESPONDING)

	def run(self):
		details = CameraDetails.FromString(self.details)
		if details.status not in [CameraStatus.CAMERA_ENABLED, CameraStatus.CAMERA_LOADING]: return
		camera = cv2.VideoCapture(self.camera_id)
		camera.set(cv2.CAP_PROP_FRAME_WIDTH, details.resolution_width)
		camera.set(cv2.CAP_PROP_FRAME_HEIGHT, details.resolution_height)
		self.set_status(CameraStatus.CAMERA_ENABLED)
		details.status = CameraStatus.CAMERA_ENABLED
		try:
			while True:
				success, frame = camera.read()
				if not success: 
					self.set_status(CameraStatus.CAMERA_NOT_RESPONDING)
					return
				self.client.send_frame(camera_id=self.camera_id, frame=frame, details=details)
				time.sleep(1/details.fps)
		except KeyboardInterrupt: pass
		except OSError as error:
			if error.errno == 10040:  # message too large
				self.set_status(CameraStatus.FRAME_TOO_LARGE)

	def copy(self): return CameraThread(
		camera_id=self.camera_id, 
		details=CameraDetails.FromString(self.details),
		client=self.client, 
		queue=self.queue
	)

def get_threads(socket, queue): return [
	CameraThread(
		camera_id=index,
		details=constants.get_default_details(index),
		client=socket,
		queue = queue,
	)
	for index in range(10)
]
