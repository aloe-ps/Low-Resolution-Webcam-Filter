import threading

import cv2
from cv2.typing import MatLike
import numpy as np

from setting.config import Config


MASK_LUT = (
    1.0 - np.arange(256, dtype=np.float32) / np.float32(255.0)
) ** np.float32(1.5)

fixed_noise = None
prev_noise = None
noise_lock = threading.Lock()

_buffers = None
_buffers_shape = None


class _Buffers:
    __slots__ = (
        "gray",
        "mask",
        "f",
        "u8",
        "hsv",
        "blur",
        "out",
        "noise_dynamic",
        "noise_current",
        "noise_mix_a",
        "noise_mix_b",
        "noise_2d",
        "chroma",
        "saturation_lut",
        "saturation_value",
    )

    def __init__(self, h, w):
        self.gray = np.empty((h, w), np.uint8)
        self.mask = np.empty((h, w), np.float32)
        self.f = np.empty((h, w, 3), np.float32)
        self.u8 = np.empty((h, w, 3), np.uint8)
        self.hsv = np.empty((h, w, 3), np.uint8)
        self.blur = np.empty((h, w, 3), np.float32)
        self.out = np.empty((h, w, 3), np.uint8)
        self.noise_dynamic = np.empty((h, w, 1), np.float32)
        self.noise_current = np.empty((h, w, 1), np.float32)
        self.noise_mix_a = np.empty((h, w, 1), np.float32)
        self.noise_mix_b = np.empty((h, w, 1), np.float32)
        self.noise_2d = np.empty((h, w), np.float32)
        self.chroma = np.empty((h, w), np.float32)
        self.saturation_lut = None
        self.saturation_value = None


def _get_buffers(h, w):
    global _buffers, _buffers_shape
    if _buffers_shape != (h, w):
        _buffers = _Buffers(h, w)
        _buffers_shape = (h, w)
    return _buffers


def _get_saturation_lut(buffers, saturation):
    if buffers.saturation_value != saturation:
        lut = np.empty((256, 1, 3), np.uint8)
        values = np.arange(256, dtype=np.uint8)
        lut[:, 0, 0] = values
        lut[:, 0, 1] = np.clip(
            np.arange(256, dtype=np.float32) * np.float32(saturation),
            0,
            255,
        ).astype(np.uint8)
        lut[:, 0, 2] = values
        buffers.saturation_lut = lut
        buffers.saturation_value = saturation
    return buffers.saturation_lut


def _clip_to_uint8(src, dst, upper):
    np.clip(src, 0, upper, out=src)
    np.copyto(dst, src, casting="unsafe")


def apply_low_resolution(frame: MatLike, config: Config):
    global fixed_noise, prev_noise

    h, w = frame.shape[:2]
    buffers = _get_buffers(h, w)

    cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, dst=buffers.gray)
    cv2.LUT(buffers.gray, MASK_LUT, dst=buffers.mask)

    f = buffers.f
    np.copyto(f, frame, casting="unsafe")

    if config.blue_gain != 1.0:
        f[:, :, 0] *= config.blue_gain
    if config.green_gain != 1.0:
        f[:, :, 1] *= config.green_gain
    if config.red_gain != 1.0:
        f[:, :, 2] *= config.red_gain

    t_factor = config.temperature * 0.2 * 255.0
    if t_factor != 0.0:
        np.multiply(buffers.mask, np.float32(t_factor), out=buffers.noise_2d)
        f[:, :, 2] += buffers.noise_2d
        f[:, :, 0] -= buffers.noise_2d

    _clip_to_uint8(f, buffers.u8, 255)
    cv2.cvtColor(buffers.u8, cv2.COLOR_BGR2HSV, dst=buffers.hsv)
    if config.saturation != 1.0:
        cv2.LUT(
            buffers.hsv,
            _get_saturation_lut(buffers, config.saturation),
            dst=buffers.hsv,
        )
    cv2.cvtColor(buffers.hsv, cv2.COLOR_HSV2BGR, dst=buffers.u8)
    np.copyto(f, buffers.u8, casting="unsafe")

    blur = buffers.blur
    kx = int(config.blur_x)
    if kx > 1:
        if kx % 2 == 0:
            kx += 1
        cv2.GaussianBlur(f, (kx, 1), 0, dst=blur)
        f, blur = blur, f

    if config.contrast != 1.0:
        f *= config.contrast
    if config.brightness != 0:
        f += config.brightness * 255.0

    with noise_lock:
        if fixed_noise is None or fixed_noise.shape[:2] != (h, w):
            fixed_noise = np.empty((h, w, 1), np.float32)
            cv2.randn(fixed_noise, 0.0, config.noise_strength * 255.0)
            prev_noise = fixed_noise.copy()

        assert prev_noise is not None

        cv2.randn(buffers.noise_dynamic, 0.0, config.noise_fine * 255.0)
        cv2.add(fixed_noise, buffers.noise_dynamic, dst=buffers.noise_current)

        if prev_noise is buffers.noise_mix_a:
            combined_noise = buffers.noise_mix_b
        else:
            combined_noise = buffers.noise_mix_a
        cv2.addWeighted(
            prev_noise,
            config.noise_alpha,
            buffers.noise_current,
            1 - config.noise_alpha,
            0,
            dst=combined_noise,
        )
        prev_noise = combined_noise

    np.multiply(combined_noise[:, :, 0], buffers.mask, out=buffers.noise_2d)
    np.add(f, buffers.noise_2d[:, :, None], out=f)

    shift = int(config.chromatic_shift)
    if shift != 0:
        channel = f[:, :, 2]
        if 0 < shift < w:
            np.copyto(buffers.chroma[:, :shift], channel[:, -shift:])
            np.copyto(buffers.chroma[:, shift:], channel[:, :-shift])
            np.copyto(channel, buffers.chroma)
        else:
            channel[:] = np.roll(channel, shift, axis=1)

    cv2.GaussianBlur(f, (3, 3), 0, dst=blur)
    cv2.addWeighted(f, 0.7, blur, 0.3, 0, dst=f)

    np.clip(f, 0, 250, out=f)
    np.copyto(buffers.out, f, casting="unsafe")
    return buffers.out
