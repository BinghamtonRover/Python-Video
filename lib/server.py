from lib.network import ProtoServer
from lib.network.generated.Protobuf.video_pb2 import *

class VideoServer(ProtoServer):
	def on_message(self, wrapper, source): 
		if wrapper.name == "AdjustCamera":
			command = AdjustCamera.FromString(wrapper.data)
			# TODO: Do something with this command
		else: print(f"Received an unknown message type: {wrapper.name}")
