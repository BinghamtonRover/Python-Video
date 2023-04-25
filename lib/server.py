from network import ProtoSocket, VideoClient
from network.generated import *

from lib.thread import get_threads
import lib.constants as constants

class VideoServer(ProtoSocket):
	def __init__(self, port):
		self.video_socket = VideoClient(compression=constants.compression, port=8003, device=Device.VIDEO)
		self.camera_threads = get_threads(self.video_socket)

		if not self.camera_threads: quit("No workable camera detected")
		else: print(f"Using cameras {[thread.camera_id for thread in self.camera_threads]}")
		super().__init__(port=port, device=Device.VIDEO)

	def on_connect(self, source): 
		print("Starting cameras")
		super().on_connect(source)
		self.video_socket.destination = (source[0], constants.dashboard_video_port)
		for thread in self.camera_threads:
			thread.start()

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
		else: raise Exception(f"Could not find camera with name={name}")

	def on_message(self, wrapper): 
		print(f"Received {wrapper.name}")
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
			if not command.is_enabled and thread.is_alive():
				thread.terminate()
				self.camera_threads[index] = thread.copy()
			elif command.is_enabled and not thread.is_alive():
				thread.start()


			# if (camEnabled[AdjustCamera.id] == 0) and (AdjustCamera.isEnabled == True):
			# 	thread = camThread("Camera", list(serials.keys())[AdjustCamera.id])
			# 	thread.start()
			# 	cam_status(camID, True)
			# 	camEnabled[AdjustCamera.id] = 1
			# elif (camEnabled[AdjustCamera.id] == 1) and (AdjustCamera.isEnabled == False):
			# 	thread.raise_exception()
			# 	cam_status(camID, False)
			# 	camEnabled[AdjustCamera.id] = 0
