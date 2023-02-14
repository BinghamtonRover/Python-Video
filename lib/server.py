from lib.network import ProtoServer
from lib.network.generated.Protobuf.wrapper_pb2 import WrappedMessage

class VideoServer(ProtoServer):
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
