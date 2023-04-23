#server to test main is sending correctly
import socket
import cv2
import imutils
import time
import base64
import numpy as np
from multiprocessing import Process
#from lib.network.bin.video_server import *
#from lib.network.src.proto_server import * 
from lib.network.generated.Protobuf.wrapper_pb2 import WrappedMessage
from lib.network.generated.Protobuf.video_pb2 import CameraName
from lib.network.generated.Protobuf.video_pb2 import CameraStatus

localIP     = "127.0.0.1"
localPort   = 8006
bufferSize  = 65536


# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("here")
UDPServerSocket.settimeout(0.5)

print("UDP server up and listening")
#server = ProtoServer(UDPServerSocket)
# Listen for incoming datagrams
try:
	while(True):
		try:
			bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
			print(bytesAddressPair);
			data = bytesAddressPair[0]
			print("data: ")
			print(data)
			wrapper = WrappedMessage.FromString(data)
			print(f"Received a {wrapper.name} message")
			print(f"Received a {wrapper.data} message")
			print(f"Received a {wrapper.data.id} message")

            # Press Q on keyboard to  exit
			if cv2.waitKey(25) & 0xFF == ord('q'):
				print("INSIDE")
				break

		except socket.timeout: pass
except KeyboardInterrupt:
	print("Closing server")


UDPServerSocket.close()
