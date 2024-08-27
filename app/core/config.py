import os


class MediaSettings:
	MEDIA_DIR = "./media"
	IMG_DIR = f"{MEDIA_DIR}/images/"

media_settings = MediaSettings()

class UploadSettings:
	MAX_UPLOAD_SIZE = 10485760 #10MB 

upload_settings = UploadSettings()