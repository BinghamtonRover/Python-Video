import threading
import cv2
import multiprocessing

from network import *
from network.generated import *

from lib.thread import get_threads
import lib.constants as constants

class VideoClient(ProtoSocket):
	def send_frame(self, camera_id, frame, details):
		encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, details.quality])
		message = VideoData(id=camera_id, details=details, frame=buffer.tobytes())
		# print(f"Sending {len(buffer)} bytes to {self.destination} for camera {CameraName.Name(details.name)}")
		self.send_message(message)

class VideoServer(ProtoSocket):
	def __init__(self, port):
		super().__init__(port=port, device=Device.VIDEO)
		self.queue = multiprocessing.Queue()
		self.client = VideoClient(port=8003, device=Device.VIDEO)
		self.camera_threads = get_threads(self.client, self.queue)

		if not self.camera_threads: quit("No workable camera detected")
		self.send_data()

	def close(self): 
		for thread in self.camera_threads: 
			if thread.is_alive(): thread.terminate()
		self.client.close()
		super().close()

	def update_settings(self, settings):
		super().update_settings(settings)
		if settings.status == RoverStatus.AUTONOMOUS: 
			# The autonomy mode needs full control over all the cameras
			for index, thread in enumerate(self.camera_threads): 
				details = CameraDetails.FromString(thread.details)
				details.status = CameraStatus.CAMERA_DISABLED
				self.overwrite_details(index, thread, details)

	def on_connect(self, source): 
		super().on_connect(source)
		self.client.on_connect(source)
		print("Starting cameras")
		self.send_data()
		for thread in self.camera_threads:
			details = CameraDetails.FromString(thread.details)
			if details.status == CameraStatus.CAMERA_DISABLED: continue
			details.status = CameraStatus.CAMERA_LOADING
			print(f"  Opening camera {CameraName.Name(details.name)}")
			thread.start()
			self.send_message(VideoData(id=thread.camera_id, details=details))

	def on_disconnect(self):
		super().on_disconnect()
		self.client.on_disconnect()
		print("Closing cameras")
		for thread in self.camera_threads:
			if thread.is_alive(): thread.terminate()
		# Keep the old settings but restart the thread
		self.camera_threads = [thread.copy() for thread in self.camera_threads]

	def send_data(self): 
		if not self.is_connected(): return

		statuses = [None] * len(self.camera_threads)
		while not self.queue.empty():  # read all data
			camera_id, status = self.queue.get()
			statuses[camera_id] = status

		for thread in self.camera_threads:
			details = CameraDetails.FromString(thread.details)
			if statuses[thread.camera_id] is not None: 
				details.status = statuses[thread.camera_id]
				thread.details = details.SerializeToString()
			data = VideoData(
				id=thread.camera_id,
				details=details,
			)
			self.send_message(data)
		self.timer = threading.Timer(1, self.send_data)
		self.timer.daemon = True
		self.timer.start()

	def overwrite_details(self, index, thread, details): 
		if thread.is_alive(): thread.terminate()
		copy = thread.copy()
		copy.details = details.SerializeToString()
		self.camera_threads[index] = copy
		self.send_message(VideoData(id=thread.camera_id, details=details))
		if details.status in [CameraStatus.CAMERA_ENABLED, CameraStatus.CAMERA_LOADING]: copy.start()

	def on_message(self, wrapper): 
		settings = UpdateSetting.FromString(self.settings)
		if settings.status == RoverStatus.AUTONOMOUS: return
		if wrapper.name == "VideoCommand": 
			# Respond to handshake
			command = VideoCommand.FromString(wrapper.data)
			self.send_message(command)
			# Send LOADING before making any changes
			thread = self.camera_threads[command.id]
			old_details = CameraDetails.FromString(thread.details)
			old_details.status = CameraStatus.CAMERA_LOADING
			self.send_message(VideoData(id=thread.camera_id, details=old_details))
			# Change the settings
			self.overwrite_details(command.id, thread, command.details)
