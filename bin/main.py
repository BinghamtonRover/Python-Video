
import cv2
import time
import subprocess
from multiprocessing import Process

from network import VideoClient, ProtoSocket
from lib.thread import *
from lib.server import VideoServer
from network.generated import *

if __name__ == '__main__':
	print("Initializing...")
	data_socket = VideoServer(port=8002)
	try: data_socket.listen()
	except KeyboardInterrupt: pass
