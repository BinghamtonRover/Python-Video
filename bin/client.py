from lib.network import ProtoClient
from lib.network.generated.Protobuf.video_pb2 import *

client = ProtoClient()
status = CameraStatus(id=3, is_enabled=True)
client.send_message("CameraStatus", status, "127.0.0.1", port=8001)
