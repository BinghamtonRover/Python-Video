import cv2
import threading
import subprocess
import socket

from Networking import ProtoSocket, VideoClient, Device
from Networking.src.generated.Protobuf.video_pb2 import *

from lib.server import VideoServer

serials = {}
FILTER = "ID_SERIAL="
camEnabled = [0,0,0,0,0,0,0]
video_socket = VideoClient(port=8000, device=Device.VIDEO, buffer=65_527)
data_socket = VideoServer(port=8001, device=Device.VIDEO)

def cam_status(camID, enabled):
	status = CameraStatus(id=camID, is_enabled=enabled)
	data_socket.send_message(status)
	
class camThread(threading.Thread):
	def __init__(self, previewName, camID):
		threading.Thread.__init__(self)
		self.previewName = previewName
		self.camID = camID
	def run(self):
		print("Starting " + self.previewName)
		camPreview(self.previewName, self.camID)

def camPreview(previewName, camID):
	cv2.namedWindow(previewName)
	cam = cv2.VideoCapture(camID)
	#Set to lower resolution for shared USB bus
	cam.set(3,320)
	cam.set(4,240)
	if cam.isOpened():  # try to get the first frame
		rval, frame = cam.read()
		cam_status(camID, True)
	else:
		rval = False

	while rval:
		#cv2.imshow(previewName, frame)
		rval, frame = cam.read()
		video_socket.send_frame(camID, frame)
		#key = cv2.waitKey(20)
		#if key == 27:  # exit on ESC
		 #   break
	#cv2.destroyWindow(previewName)
	cam_status(camID, False)

def get_cam_serial(cam_id):
	# Only works on Linux
	p = subprocess.Popen('udevadm info --name=/dev/video{} | grep {} | cut -d "=" -f 2'.format(cam_id, FILTER),
						 stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	p.status = p.wait()
	response = output.decode('utf-8')
	return response.replace('\n', '')

if __name__ == '__main__':
	import platform
	# TODO: Make a simple test for Windows
	if (platform.system() != "Linux"):
		print("Sorry, this script only works on Linux")
		quit()

	for cam_id in range(0, 20, 2):
		serial = get_cam_serial(cam_id)
		if len(serial) > 6:
			serials[cam_id] = serial

	for key in serials:
		cam_status(key,False)

	print('Cam ID:', serials.keys())
	print('Cam Names: ', serials.values())

	server.listen()
#while:
#    message = server.on_data(
# Create two threads as follows
# thread1 = camThread("Camera 1", list(serials.keys())[0])
# thread2 = camThread("Camera 2", list(serials.keys())[1])
# thread1.start()
# thread2.start()
