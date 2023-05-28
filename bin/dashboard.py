"""
This code is a demo ONLY. Use the dashboard to display video.

This script can display video, but the dashboard can modify the camera settings.
"""

import cv2
import numpy
import socket
import threading

from network import ProtoSocket
from network.generated import *

heartbeat = Connect(sender=Device.DASHBOARD, receiver=Device.VIDEO)

class VideoServer(ProtoSocket):
	def __init__(self, port): 
		super().__init__(port, device=Device.DASHBOARD, buffer=65_527, destination=("127.0.0.1", 8002))

	# Make sure waitKey is called every once in a while
	def on_loop(self): 
		if cv2.waitKey(1) == ord("q"): self.close()

	# Override of ProtoSocket.close()
	def close(self): 
		cv2.destroyAllWindows()
		super().close()

	# Override of ProtoSocket.on_message
	def on_message(self, wrapper): 
		if wrapper.name == VideoData.DESCRIPTOR.name:
			data = VideoData.FromString(wrapper.data)
			if not data.frame: return
			array = numpy.frombuffer(data.frame, dtype="uint8")
			name = CameraName.Name(data.details.name)
			frame = cv2.imdecode(array, 1)
			cv2.imshow(name, frame)

if __name__ == "__main__":
	video_server = VideoServer(port=8008)

	def send_heartbeat():
		video_server.send_message(heartbeat)
		timer = threading.Timer(0.2, send_heartbeat)
		timer.daemon = True
		timer.start()
	send_heartbeat()

	video_server.listen()
