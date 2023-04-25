from network.generated import *

# The resolution to start streaming at, once the dashboard is connected.
default_resolution = (400, 400)

# These list maps OpenCV IDs (index) to [CameraName]s. 
# 
# This is HIGHLY dependent on the EXACT order of the USB ports.
camera_names = [
	CameraName.ROVER_FRONT, 
	CameraName.ROVER_REAR,
	CameraName.ARM_BASE,
	CameraName.ARM_GRIPPER,
	CameraName.CAMERA_NAME_UNDEFINED,
	CameraName.CAMERA_NAME_UNDEFINED,
	CameraName.CAMERA_NAME_UNDEFINED,
	CameraName.CAMERA_NAME_UNDEFINED,
	CameraName.CAMERA_NAME_UNDEFINED,
	CameraName.CAMERA_NAME_UNDEFINED,
	CameraName.CAMERA_NAME_UNDEFINED,
]

dashboard_video_port = 8008

framerate = 1/30  # FPS
compression = 50  # 1-100
