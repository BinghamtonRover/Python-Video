from network.generated import *

# These list maps OpenCV IDs (index) to [CameraName]s. 
# 
# This is HIGHLY dependent on the EXACT order of the USB ports.
camera_names = {
	"/dev/realsense_rgb": CameraName.ROVER_FRONT,
	"/dev/realsense_depth": CameraName.AUTONOMY_DEPTH,
	"/dev/subsystem1": CameraName.SUBSYSTEM1,
	"/dev/subsystem2": CameraName.SUBSYSTEM2,
	"/dev/subsystem3": CameraName.SUBSYSTEM3,
}

def get_default_details(index): return CameraDetails(
	name=camera_names[index],
	resolution_width=300,
	resolution_height=300,
	quality=50,
	fps=24,
	status=CameraStatus.CAMERA_ENABLED,
)
