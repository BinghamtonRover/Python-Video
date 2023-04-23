from Networking import ProtoSocket
from Networking.src.generated.Protobuf.wrapper_pb2 import WrappedMessage

class VideoServer(ProtoSocket):
	def on_message(self, wrapper, source): 
		if wrapper.name == "AdjustCamera":
			command = AdjustCamera.FromString(wrapper.data)

		if (camEnabled[AdjustCamera.id] == 0) and (AdjustCamera.isEnabled == True):
			thread = camThread("Camera", list(serials.keys())[AdjustCamera.id])
			thread.start()
			cam_status(camID, True)
			camEnabled[AdjustCamera.id] = 1
		elif (camEnabled[AdjustCamera.id] == 1) and (AdjustCamera.isEnabled == False):
			thread.raise_exception()
			cam_status(camID, False)
			camEnabled[AdjustCamera.id] = 0
