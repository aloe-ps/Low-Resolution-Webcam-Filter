import threading
import cv2
from cv2.typing import MatLike
import numpy as np
from setting.config import Config

fixed_noise = None
prev_noise = None
noise_lock = threading.Lock()

def apply_low_resolution(frame: MatLike, config: Config):
    global fixed_noise, prev_noise

    h, w = frame.shape[:2]

    # Grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_f = gray.astype(np.float32) / 255.0
    mask = (1.0 - gray_f) ** 1.5

    # Color
    f = frame.astype(np.float32)
    
    if config.blue_gain != 1.0: f[:,:,0] *= config.blue_gain
    if config.green_gain != 1.0: f[:,:,1] *= config.green_gain
    if config.red_gain != 1.0: f[:,:,2] *= config.red_gain

    t_factor = config.temperature * 0.2 * 255.0 # 定数部分を事前に計算
    f[:,:,2] += t_factor * mask
    f[:,:,0] -= t_factor * mask

    # Saturation
    f_uint8 = np.clip(f, 0, 255).astype(np.uint8)
    hsv = cv2.cvtColor(f_uint8, cv2.COLOR_BGR2HSV)
    if config.saturation != 1.0:
        s = hsv[:,:,1].astype(np.float32) * config.saturation
        hsv[:,:,1] = np.clip(s, 0, 255).astype(np.uint8)
    f = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR).astype(np.float32)

    # Blur
    kx = int(config.blur_x)
    if kx > 1:
        if kx % 2 == 0: kx += 1
        f = cv2.GaussianBlur(f, (kx, 1), 0)

    # Contrast, Brightness
    if config.contrast != 1.0 or config.brightness != 0:
        f = f * config.contrast + (config.brightness * 255.0)

    # Active Noise
    with noise_lock:
        if fixed_noise is None or fixed_noise.shape[:2] != (h, w):
            fixed_noise = np.random.normal(0, config.noise_strength * 255.0, (h, w, 1)).astype(np.float32)
            prev_noise = fixed_noise.copy()
        
        assert prev_noise is not None

        dynamic_noise = np.random.normal(0, config.noise_fine * 255.0, (h, w, 1)).astype(np.float32)
        current_noise = fixed_noise + dynamic_noise
        
        combined_noise = prev_noise * config.noise_alpha + current_noise * (1 - config.noise_alpha)
        prev_noise = combined_noise

    f += combined_noise * mask[..., None]
    
    # Chromatic shift
    if config.chromatic_shift != 0:
        f[:,:,2] = np.roll(f[:,:,2], int(config.chromatic_shift), axis=1)

    # Noise
    blur = cv2.GaussianBlur(f, (3, 3), 0)
    f = f * 0.7 + blur * 0.3

    return np.clip(f, 0, 250).astype(np.uint8)