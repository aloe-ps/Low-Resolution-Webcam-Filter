import cv2
import pyvirtualcam
import threading

from ui import start_ui
from filter import apply_low_resolution
from config import config


def camera_loop():
    cap = cv2.VideoCapture(0)

    width = int(cap.get(3))
    height = int(cap.get(4))

    with pyvirtualcam.Camera(width=width, height=height, fps=30) as cam:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            processed = apply_low_resolution(frame, config)

            cam.send(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB))
            cam.sleep_until_next_frame()


# カメラは別スレッド
threading.Thread(target=camera_loop, daemon=True).start()

# UIはメインスレッド
start_ui(config)