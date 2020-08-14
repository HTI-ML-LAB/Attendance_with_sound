import cv2
from BaseCamera import BaseCamera

from easydict import EasyDict as edict

class Camera(BaseCamera):
   
    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames(unique_id):
        t=0
        #global face
        # camera = cv2.VideoCapture("rtsp://admin:adminFZCAVL@192.168.100.249/ISAPI/Streaming/channels/101")
        camera = cv2.VideoCapture(0)
        # camera.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
        # camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            _, frame = camera.read()      
            yield frame
