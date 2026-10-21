import cv2
import pyvirtualcam
import threading

from filter import apply_low_resolution
from setting.config import config
from ui.run import start_ui


def camera_loop():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    width = int(cap.get(3))
    height = int(cap.get(4))

    with pyvirtualcam.Camera(
        width=width,
        height=height,
        fps=30,
        fmt=pyvirtualcam.PixelFormat.BGR,
    ) as cam:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            processed = apply_low_resolution(frame, config)

            cam.send(processed)
            cam.sleep_until_next_frame()


# カメラは別スレッド
threading.Thread(target=camera_loop, daemon=True).start()

# UIはメインスレッド
start_ui(config)