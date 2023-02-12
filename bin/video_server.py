from .udp_server import UdpServer
from .proto_server import ProtoServer

from lib.network.generated.Protobuf.wrapper_pb2 import WrappedMessage

class VideoServer(ProtoServer):
	#def on_message(self, data, source): 
	#	wrapper = WrappedMessage.FromString(data)
	#	self.on_message(wrapper, source)

	# Can override this in a subclass
	def on_message(self, wrapper, source): 
		if wrapper.name == "AdjustCamera":
			command = AdjustCamera.FromString(wrapper.data)
