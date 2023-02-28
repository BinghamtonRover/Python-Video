import cv2
import time
import subprocess
from multiprocessing import Process

from lib.network import VideoClient, ProtoClient
from lib.network.generated.Protobuf.video_pb2 import *

RESOLUTION = (400, 400)
cv2.setLogLevel(0)  # no logging from OpenCV

CAMERAS = [
	CameraName.CAMERA_NAME_ROVER_FRONT, 
	CameraName.CAMERA_NAME_ROVER_REAR,
	CameraName.CAMERA_NAME_ARM_BASE,
	CameraName.CAMERA_NAME_ARM_GRIPPER,
	CameraName.CAMERA_NAME_UNDEFINED
]

class CameraThread(Process):
	def __init__(self, name, id, client):
		print(f"Initializing camera {id}")
		self.camera_name = name
		self.id = id
		self.camera = cv2.VideoCapture(id)
		self.client = client
		super().__init__()
		self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, RESOLUTION[0])
		self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, RESOLUTION[1])

	def can_read(self): 
		if not self.camera.isOpened(): return False
		success, frame = self.camera.read()
		if not success: 
			print(f"Camera {self.id} is open but not responding")
		return success

	def run(self):
		try:
			while True:
				success, frame = self.camera.read()
				if not success: 
					print(f"Could not read frame for camera {self.id}")
					return
				self.client.send_frame(self.camera_name, frame)
				time.sleep(1/60)
		except KeyboardInterrupt: pass

	def get_serial(self): 
		# NOT CURRENTLY WORKING
		raise Exception("Cameras do not have unique serial numbers, do not call this method.")
		process = subprocess.Popen(
			'udevadm info --name=/dev/video{} | grep ID_SERIAL= | cut -d "=" -f 2'.format(self.id),
			stdout=subprocess.PIPE, 
			shell=True,
		)
		(output, error) = process.communicate()
		process.status = process.wait()
		response = output.decode("utf-8")
		return response.replace("\n", "")

	def close(self): 
		print(f"Closing camera {self.id}")
		self.terminate()
		time.sleep(0.5)
		self.camera.release()
		super().close()

def get_threads(): 
	threads = []
	client = VideoClient(address="192.168.1.10", port=8009)
	cams = 0
	for index in range(10):
		thread = CameraThread(CAMERAS[len(threads)], index, client)
		if thread.can_read(): threads.append(thread)
	return threads

def main(threads): 
	client = ProtoClient(address="192.168.1.10", port=8008)
	for camera in CameraName.values(): 
		# camera is an ID, 0-6
		if any(thread.camera_name == camera for thread in threads): 
			print(f"Has cam")
		else: print("Does not have cam")
	data = [
		CameraStatus(
			id=camera, 
			is_enabled=any(thread.camera_name == camera for thread in threads),
			resolution=RESOLUTION[0]
		)
		for camera in CameraName.values()
	]
	message = VideoData(cameras=data)
	while True: 
		print("Sending message")
		# client.send_message(message)
		time.sleep(1)

if __name__ == '__main__':
	print("Initializing...")
	threads = get_threads()
	if not threads: quit("No workable camera detected")
	print(f"Using cameras {[thread.id for thread in threads]}")
	try: 
		main(threads)
		# for thread in threads: thread.start()
		# for thread in threads: thread.join()
	except KeyboardInterrupt: pass
	finally: 
		for thread in threads: thread.close()
