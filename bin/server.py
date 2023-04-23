from lib.server import VideoServer
from Networking import Device

server = VideoServer(port=8002, device=Device.VIDEO)
server.listen()
