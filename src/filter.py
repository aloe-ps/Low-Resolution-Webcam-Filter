import cv2
import numpy as np

fixed_noise = None
prev_noise = None

def apply_low_resolution(frame, config):
    global fixed_noise, prev_noise

    f = frame.astype(np.float32) / 255.0
    h, w = f.shape[:2]

    # --- 色
    f[:,:,1] *= config.green_gain
    f[:,:,2] *= config.red_gain

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

    # --- ノイズ
    if fixed_noise is None:
        fixed_noise = np.random.normal(0, config.noise_strength, (h, w, 1)).astype(np.float32)

    dynamic_noise = np.random.normal(0, config.noise_fine, (h, w, 1)).astype(np.float32)
    noise = fixed_noise + dynamic_noise

    if prev_noise is None:
        prev_noise = noise

    noise = prev_noise * config.noise_alpha + noise * (1 - config.noise_alpha)
    prev_noise = noise

    # 明るさ依存
    gray = cv2.cvtColor((f*255).astype(np.uint8), cv2.COLOR_BGR2GRAY) / 255.0
    noise_strength = (1 - gray)**1.5

    f = f + noise * noise_strength[..., None]

    # --- 色収差
    b, g, r = cv2.split(f)
    r = np.roll(r, int(config.chromatic_shift), axis=1)
    f = cv2.merge((b, g, r))

    # --- にじみ
    blur = cv2.GaussianBlur(f, (3,3), 0)
    f = f * 0.7 + blur * 0.3

    f = np.clip(f, 0, 0.98)
    return (f * 255).astype(np.uint8)