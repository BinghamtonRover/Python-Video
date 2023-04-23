from lib.network.generated.Protobuf.wrapper_pb2 import WrappedMessage
#from lib.network import VideoClient
#from lib.network.generated.Protobuf.video_pb2 import *
import socket
import imutils
import cv2
import time
from multiprocessing import Process
from lib.network.bin.video_client import *
from lib.network.src.proto_client import * 
from lib.network.generated.Protobuf.video_pb2 import CameraName
from lib.network.generated.Protobuf.video_pb2 import CameraStatus

Port = 8006
statuses = [0,0,0,0,0,0,0,0];
statuses = [False,False,False,False,False,False,False,False];
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
serverAddressPort   = ("127.0.0.1", Port)
sender = ProtoClient(UDPClientSocket)
def sendStatus(p, s, r):
	n = CameraName.CAMERA_NAME_ROVER_FRONT
	message = CameraStatus(
		id=n, 
		is_enabled=s,
		resolution=r
	)
	print("message: ")
	print(message)
	sender.send_message(message, "127.0.0.1", Port)
	print("sent")
	#UDPClientSocket.sendto(message, serverAddressPort)
	
	
	
possibleThreads = []
for index in range(1):
    possibleThreads.append(CameraThread(f"Camera {index}", index, VideoClient(address="127.0.0.1", port=Port)))
    
i = 0
for thread in possibleThreads:    
	if thread.can_read():
		print("index " + str(i) + " true") 
		if (statuses[i] == False): #don't change camera status unless it's physically plugged in
			statuses[i] = True;   
	else:
		print("index " + str(i) + " false")
		statuses[i] = False;
	i += 1
	sendStatus(i, 1, 1234);
UDPClientSocket.close();
	
		