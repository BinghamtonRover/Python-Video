from lib.server import VideoServer
from network import Device

server = VideoServer(port=8002, device=Device.VIDEO)
server.listen()
