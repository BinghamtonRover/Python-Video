from .udp_server import UdpServer
from .proto_server import ProtoServer

from Networking.generated.Protobuf.wrapper_pb2 import WrappedMessage

class VideoServer(ProtoServer):
	#def on_message(self, data, source): 
	#	wrapper = WrappedMessage.FromString(data)
	#	self.on_message(wrapper, source)

	# Can override this in a subclass
	def on_message(self, wrapper, source): 
		if wrapper.name == "AdjustCamera":
			command = AdjustCamera.FromString(wrapper.data)

		if (camEnabled[AdjustCamera.id] == 0) && (AdjustCamera.isEnabled == True)
			thread = camThread("Camera", list(serials.keys())[AdjustCamera.id])
			thread.start()
			cam_status(camID, True)
			camEnabled[AdjustCamera.id] = 1
		elif (camEnabled[AdjustCamera.id] == 1) && (AdjustCamera.isEnabled == False)
			thread.raise_exception()
			cam_status(camID, False)
			camEnabled[AdjustCamera.id] = 0

