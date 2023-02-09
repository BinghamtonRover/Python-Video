from lib.network import ProtoServer
from lib.network.generated.Protobuf.video_pb2 import *

server = ProtoServer(8001)
server.start()

