from network.generated import *

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

def get_default_details(index): return CameraDetails(
	name=camera_names[index],
	resolution_width=400,
	resolution_height=400,
	quality=70,
	fps=120,
	status=CameraStatus.CAMERA_ENABLED,
)
