from multiprocessing import Queue
import threading

from network import ProtoSocket, VideoClient
from network.generated import *

from lib.thread import get_threads
import lib.constants as constants

class VideoServer(ProtoSocket):
	def __init__(self, port):
		super().__init__(port=port, device=Device.VIDEO)
		self.video_socket = VideoClient(port=8003, device=Device.VIDEO)
		self.queue = Queue()
		self.camera_threads = get_threads(self.video_socket, self.queue)

		if not self.camera_threads: quit("No workable camera detected")
		self.send_data()

	def close(self): 
		for thread in self.camera_threads: 
			if thread.is_alive(): thread.terminate()
		self.video_socket.close()
		super().close()

	def on_connect(self, source): 
		super().on_connect(source)
		print("Starting cameras")
		self.video_socket.destination = (source[0], constants.dashboard_video_port)
		self.send_data()
		for thread in self.camera_threads:
			details = CameraDetails.FromString(thread.details)
			if details.status not in [CameraStatus.CAMERA_ENABLED, CameraStatus.CAMERA_LOADING]: continue
			details.status = CameraStatus.CAMERA_LOADING
			thread.start()
			self.send_message(VideoData(id=thread.camera_id, details=details))

	def on_disconnect(self):
		super().on_disconnect()
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

	def on_message(self, wrapper): 
		if wrapper.name == "VideoCommand": 
			command = VideoCommand.FromString(wrapper.data)
			self.send_message(command)
			thread = self.camera_threads[command.id]
			old_details = CameraDetails.FromString(thread.details)

			old_details.status = CameraStatus.CAMERA_LOADING
			self.send_message(VideoData(id=thread.camera_id, details=old_details))
			if thread.is_alive(): thread.terminate()
			copy = thread.copy()
			copy.details = command.details.SerializeToString()
			self.camera_threads[command.id] = copy

			if command.details.status == CameraStatus.CAMERA_ENABLED: copy.start()
