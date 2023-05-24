from network import *
from lib.server import VideoServer

if __name__ == '__main__':
	print("Initializing...")
	socket = VideoServer(port=8002)
	thread = ServerThread(socket)
	ServerThread.startThreads([thread])
