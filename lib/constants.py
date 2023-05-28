from network.generated import *

# These list maps OpenCV IDs (index) to [CameraName]s. 
# 
# This is HIGHLY dependent on the EXACT order of the USB ports.
camera_names = {
    0: CameraName.ROVER_REAR,
    22: CameraName.AUTONOMY_DEPTH,
    24: CameraName.ROVER_FRONT,
    9: CameraName.SCIENCE_CAROUSEL,
    2: CameraName.SCIENCE_VACUUM,
    4: CameraName.SCIENCE_MICROSCOPE,
}

def get_default_details(index): return CameraDetails(
	name=camera_names[index],
	resolution_width=300,
	resolution_height=300,
	quality=50,
	fps=24,
	status=CameraStatus.CAMERA_ENABLED,
)
