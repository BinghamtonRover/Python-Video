from network.generated import *

# These list maps OpenCV IDs (index) to [CameraName]s. 
# 
# This is HIGHLY dependent on the EXACT order of the USB ports.
camera_names = [
	CameraName.ROVER_FRONT,
	CameraName.CAMERA_NAME_UNDEFINED,
	CameraName.CAMERA_NAME_UNDEFINED,
	CameraName.CAMERA_NAME_UNDEFINED,
	CameraName.ARM_BASE,
	CameraName.CAMERA_NAME_UNDEFINED,
	CameraName.ROVER_REAR,
	CameraName.CAMERA_NAME_UNDEFINED,
	CameraName.CAMERA_NAME_UNDEFINED,
	CameraName.CAMERA_NAME_UNDEFINED,
	CameraName.CAMERA_NAME_UNDEFINED,
	CameraName.CAMERA_NAME_UNDEFINED,
	CameraName.CAMERA_NAME_UNDEFINED,
]

def get_default_details(index): return CameraDetails(
	name=camera_names[index],
	resolution_width=600,
	resolution_height=600,
	quality=75,
	fps=24,
	status=CameraStatus.CAMERA_ENABLED,
)
