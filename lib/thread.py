from multiprocessing import Process, Queue
from threading import Thread, Timer

import time
import cv2

from network.generated import *
import lib.constants as constants

cv2.setLogLevel(0)  # no logging from OpenCV

class CameraThread(Process):
	def __init__(self, camera_id, details, client, queue):
		print(f"[CameraThread] Initializing camera {camera_id}: ", end="")
		self.queue = queue
		self.camera_id = camera_id
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
			print("Not connected")
		else: 
			success, frame = camera.read()
			if success: 
				print("Operational")
			else: 
				self.set_status(CameraStatus.CAMERA_NOT_RESPONDING)
				print("Not responding")

	def run(self):
		details = CameraDetails.FromString(self.details)
		if details.status not in [CameraStatus.CAMERA_ENABLED, CameraStatus.CAMERA_LOADING]: return
		camera = cv2.VideoCapture(self.camera_id)
		camera.set(cv2.CAP_PROP_FRAME_WIDTH, details.resolution_width)
		camera.set(cv2.CAP_PROP_FRAME_HEIGHT, details.resolution_height)
		self.set_status(CameraStatus.CAMERA_ENABLED)
		details.status = CameraStatus.CAMERA_ENABLED
		try:
			print(f"  Streaming camera id={self.camera_id}")
			while True:
				success, frame = camera.read()
				if not success: 
					print(f"Camera {CameraName.Name(details.name)} isn't responding!")
					self.set_status(CameraStatus.CAMERA_NOT_RESPONDING)
					time.sleep(0.5)
					return
				self.client.send_frame(camera_id=self.camera_id, frame=frame, details=details)
				if details.fps != 0: time.sleep(1/details.fps)
		except KeyboardInterrupt: pass
		except OSError as error:
			if error.errno == 10040:  # message too large
				self.set_status(CameraStatus.FRAME_TOO_LARGE)
			else: raise error
		finally:
			self.set_status(CameraStatus.CAMERA_NOT_RESPONDING)

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
