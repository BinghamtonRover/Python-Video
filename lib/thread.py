from network.generated import VideoCommand
import cv2
from multiprocessing import Process, Queue
from threading import Thread
import time

from network.generated import *
from network import VideoClient
import lib.constants as constants

cv2.setLogLevel(0)  # no logging from OpenCV

class CameraThread(Process):
	def __init__(self, camera_id, details, client, queue):
		print(f"[CameraThread] Initializing camera {camera_id}")
		self.camera_id = camera_id
		self.details = details.SerializeToString()
		self.client = client
		self.queue = queue
		self.check_camera()
		super().__init__()

	def check_camera(self): 
		result = None
		camera = cv2.VideoCapture(self.camera_id)
		if not camera.isOpened(): 
			result = CameraStatus.CAMERA_DISCONNECTED
		else: 
			success, frame = camera.read()
			if not success: 
				result = CameraStatus.CAMERA_NOT_RESPONDING
		if result is not None: 
			self.queue.put([self.camera_id, result])
			details = CameraDetails.FromString(self.details)
			details.status = result
			self.details = details.SerializeToString()

	def run(self):
		details = CameraDetails.FromString(self.details)
		if details.status != CameraStatus.CAMERA_ENABLED: return
		camera = cv2.VideoCapture(self.camera_id)
		camera.set(cv2.CAP_PROP_FRAME_WIDTH, details.resolution_width)
		camera.set(cv2.CAP_PROP_FRAME_HEIGHT, details.resolution_height)
		try:
			while True:
				success, frame = camera.read()
				if not success: 
					self.queue.put([self.camera_id, CameraStatus.CAMERA_NOT_RESPONDING])
					return
				self.client.send_frame(camera_id=self.camera_id, frame=frame, details=details)
				time.sleep(1/details.fps)
		except KeyboardInterrupt: pass

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
