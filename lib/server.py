import threading

from network import ProtoSocket, VideoClient
from network.generated import *

from lib.thread import get_threads
import lib.constants as constants

class VideoServer(ProtoSocket):
	def __init__(self, port):
		super().__init__(port=port, device=Device.VIDEO)
		self.video_socket = VideoClient(compression=constants.compression, port=8003, device=Device.VIDEO)
		self.camera_threads = get_threads(self.video_socket)

		if not self.camera_threads: quit("No workable camera detected")
		else: print(f"Using cameras {[thread.camera_id for thread in self.camera_threads]}")
		self.send_data()

	def on_connect(self, source): 
		print("Starting cameras")
		super().on_connect(source)
		self.video_socket.destination = (source[0], constants.dashboard_video_port)
		for thread in self.camera_threads:
			thread.start()
		self.send_data()

	def on_disconnect(self):
		print("Closing cameras")
		super().on_disconnect()
		for thread in self.camera_threads:
			thread.terminate()
		# Threads cannot be restarted, so make a copy instead!
		self.camera_threads = get_threads(self.video_socket)

	def get_thread(self, name): 
		for index, thread in enumerate(self.camera_threads): 
			if thread.camera_name == name: return index, thread
		else: return -1, None

	def send_data(self): 
		if not self.is_connected(): return
		for camera in CameraName.values(): 
			index, thread = self.get_thread(camera)
			is_enabled = False if thread is None else thread.is_alive() 
			data = CameraStatus(name=camera, is_connected=thread is not None, is_enabled=is_enabled)
			self.send_message(data)
		self.timer = threading.Timer(1, self.send_data)
		self.timer.daemon = True
		self.timer.start()

	def on_message(self, wrapper): 
		if wrapper.name == "VideoCommand": 
			command = VideoCommand.FromString(wrapper.data)
			print(f"Received video command: {command.compression}% compression at {command.framerate} seconds between frames");
			self.video_socket.compression = command.compression
			constants.framerate = command.framerate
			dashboard = self.destination
			self.on_disconnect()
			self.on_connect(dashboard)
		elif wrapper.name == "AdjustCamera":
			command = AdjustCamera.FromString(wrapper.data)
			index, thread = self.get_thread(command.name)
			if not command.enable and thread.is_alive():
				thread.terminate()
				self.camera_threads[index] = thread.copy()
			elif command.enable and not thread.is_alive():
				thread.start()
