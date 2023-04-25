
import cv2
import time
import subprocess
from multiprocessing import Process

from network import VideoClient, ProtoSocket
from lib.thread import *
from lib.server import VideoServer
from network.generated import *

def main(threads): 
	# for camera in CameraName.values():
	# 	# camera is an ID, 0-6
	# 	if any(thread.camera_name == camera for thread in threads): 
	# 		print(f"Has cam")
	# 	else: print("Does not have cam")
	# data = [
	# 	CameraStatus(
	# 		name=camera, 
	# 		is_enabled=any(thread.camera_name == camera for thread in threads),
	# 		resolution=constants.default_resolution[0]
	# 	)
	# 	for camera in CameraName.values()
	# ]
	# data_socket.listen()
	# message = VideoData(cameras=data)
	while True: pass

if __name__ == '__main__':
	print("Initializing...")
	data_socket = VideoServer(port=8002)
	# threads = get_threads(video_socket)
	# if not threads: quit("No workable camera detected")
	try: 
		data_socket.listen()
	except KeyboardInterrupt: pass
