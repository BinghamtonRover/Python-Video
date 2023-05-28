import threading
import time
import cv2

from network.generated import *
import lib.constants as constants

cv2.setLogLevel(0)  # no logging from OpenCV

class CameraThread(threading.Thread):
	def __init__(self, camera_id, details, collection):
		print(f"[CameraThread] Initializing camera {camera_id}: ", end="")
		self.camera_id = camera_id
		self.details = details
		self.collection = collection
		self.keep_alive = True
		self.camera = cv2.VideoCapture(camera_id)
		self.update_details(details)
		self.check_camera()
		super().__init__()
		
	def spaces(self): return " " * self.camera_id
	def close(self): self.keep_alive = False

	def set_status(self, status):
		self.details.status = status
		self.collection.server.send_status(self.camera_id, status)

	def check_camera(self):
		if not self.camera.isOpened():  # check if the camera is even connected
			self.set_status(CameraStatus.CAMERA_DISCONNECTED)
			print("Not connected")
		else:  # try to read a frame
			success, frame = self.camera.read()
			if success:
				print("Operational")
			else: 
				self.set_status(CameraStatus.CAMERA_NOT_RESPONDING)
				print("Not responding")

	def send_frame(self, frame):
		server = self.collection.server
		if not server.is_connected(): return
		encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, self.details.quality])
		message = VideoData(id=self.camera_id, details=self.details, frame=buffer.tobytes())
		# print(f"Sending {len(buffer)} bytes to {server.destination} for camera {CameraName.Name(self.details.name)} at {self.details.quality}% quality")
		server.send_message(message)
		
	def update_details(self, details):
		status = details.status
		self.details = details
		self.set_status(CameraStatus.CAMERA_LOADING)
		time.sleep(0.5)
		self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, details.resolution_width)
		self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, details.resolution_height)
		time.sleep(0.5)
		self.details.status = status

	def run(self):
		name = CameraName.Name(self.details.name)
		server = self.collection.server
		print(f"{self.spaces()}Thread spawned for camera {name}")
		while self.keep_alive:
			if self.details.fps != 0: time.sleep(1/self.details.fps)
			# Send data about this camera
			if name == CameraName.CAMERA_NAME_UNDEFINED: 
				print(f"{self.spaces()}Quitting because camera id={self.camera_id} has no name")
				self.set_status(CameraStatus.CAMERA_HAS_NO_NAME)
			data = VideoData(id=self.camera_id, details=self.details)
			server.send_message(data)
			# Stream video
			if self.details.status != CameraStatus.CAMERA_ENABLED or not server.is_connected(): continue
			success, frame = self.camera.read()
			if success:
				try:
					self.send_frame(frame=frame)
				except OSError as error:
					if error.errno in [90, 10040]:  # message too large
						self.set_status(CameraStatus.FRAME_TOO_LARGE)
					else: 
						self.set_status(CameraStatus.CAMERA_NOT_RESPONDING)
						raise error
			else:
				print(f"{self.spaces()}Camera {name} isn't responding!")
				self.set_status(CameraStatus.CAMERA_NOT_RESPONDING)
				continue

def get_threads(collection): return {
    index: CameraThread(
		camera_id=index,
		details=constants.get_default_details(index),
		collection=collection,
	)
	for index in constants.camera_names
}
