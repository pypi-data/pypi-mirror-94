import cv2
from typing import Union, Callable


class Camera:
    def __init__(self, camera_id: Union[int, str] = 0,
                 frame_callback: Callable = None):
        self.camera_id = camera_id
        self.video = cv2.VideoCapture(self.camera_id)
        self.frame_callback = frame_callback

    def __del__(self):
        self.video.release()

    def get_frame(self):
        _, frame = self.video.read()
        try:
            frame = self.frame_callback(frame)
        except TypeError:
            pass
        return frame

    def get_stream(self):
        while self.video.isOpened():
            frame = self.get_frame()
            _, jpeg = cv2.imencode('.jpg', frame)
            frame = jpeg.tobytes() or b''
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n'
                   + frame
                   + b'\r\n')
