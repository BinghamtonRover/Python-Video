import cv2
import multiprocessing

from network import *
from network.generated import *

class VideoServer(ProtoSocket):
	def __init__(self, port, collection):  # Overriden from ProtoSocket
		self.collection = collection
		super().__init__(port=port, device=Device.VIDEO)
		
	def send_status(self, camera_id, status):
		data = VideoData(id=camera_id, details=CameraDetails(status=status))
		self.send_message(data)

	def update_settings(self, settings):  # Overriden from ProtoSocket
		super().update_settings(settings)
		if settings.status == RoverStatus.AUTONOMOUS:
			# The autonomy mode needs full control over all the cameras
			for thread in self.collection.cameras.values():
				thread.details.status = CameraStatus.CAMERA_DISABLED
				thread.close()

	def send_message(self, message):  # Overriden from ProtoSocket
		if not self.is_connected(): return
		super().send_message(message)

	def on_message(self, wrapper): 
		settings = UpdateSetting.FromString(self.settings)
		if settings.status == RoverStatus.AUTONOMOUS: return
		if wrapper.name == "VideoCommand":
			# Respond to handshake
			command = VideoCommand.FromString(wrapper.data)
			self.send_message(command)
			# Send LOADING before making any changes
			thread = self.collection.cameras[command.id]
			self.send_status(thread.camera_id, CameraStatus.CAMERA_LOADING)
			# Change the settings
			thread.update_details(command.details)
			return
			thread.close()
			time.sleep(0.5)
			thread.restart()
