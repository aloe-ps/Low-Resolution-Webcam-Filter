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

    f = frame.astype(np.float32) / 255.0
    h, w = f.shape[:2]

    with noise_lock:
        if fixed_noise is None or fixed_noise.shape[:2] != (h, w):
            fixed_noise = np.random.normal(0, config.noise_strength, (h, w, 1)).astype(np.float32)
        if prev_noise is None or prev_noise.shape[:2] != (h, w):
            prev_noise = fixed_noise.copy()
            
    # --- 色
    f[:,:,0] *= config.blue_gain
    f[:,:,1] *= config.green_gain
    f[:,:,2] *= config.red_gain

    f = np.clip(f, 0, 1.0)
    t = config.temperature
    gray = cv2.cvtColor((f*255).astype(np.uint8), cv2.COLOR_BGR2GRAY) / 255.0
    mask = (1.0 - gray) ** 1.5
    f[:,:,2] *= (1.0 + t * 0.2 * mask)
    f[:,:,0] *= (1.0 - t * 0.2 * mask)
    f = np.clip(f, 0, 1.0)

    # --- 彩度
    hsv = cv2.cvtColor((f*255).astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:,:,1] *= config.saturation
    hsv = np.clip(hsv, 0, 255).astype(np.uint8)
    f = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR).astype(np.float32) / 255.0

    # --- ブラー
    kx = int(config.blur_x)
    if kx % 2 == 0: kx += 1
    f = cv2.GaussianBlur(f, (kx,1), 0)

    # --- コントラスト
    f = f * config.contrast + config.brightness
    f = np.clip(f, 0, 1.0)

    # --- 動的ノイズの計算
    dynamic_noise = np.random.normal(0, config.noise_fine, (h, w, 1)).astype(np.float32)
    
    with noise_lock:
        if fixed_noise is None:
            fixed_noise = np.random.normal(0, config.noise_strength, (h, w, 1)).astype(np.float32)
        
        current_noise = fixed_noise + dynamic_noise
        
        if prev_noise is None:
            prev_noise = current_noise
        
        combined_noise = prev_noise * config.noise_alpha + current_noise * (1 - config.noise_alpha)
        prev_noise = combined_noise

    # 明るさ依存
    noise_strength = (1 - gray)**1.5
    f = f + combined_noise * noise_strength[..., None]
    
    # --- 色収差
    f_float32 = f.astype(np.float32)
    b, g, r = cv2.split(f_float32)
    r = np.roll(r, int(config.chromatic_shift), axis=1)
    f = cv2.merge((b, g, r))

    # --- にじみ
    blur = cv2.GaussianBlur(f, (3,3), 0)
    f = f * 0.7 + blur * 0.3

    f = np.clip(f, 0, 0.98)
    return (f * 255).astype(np.uint8)