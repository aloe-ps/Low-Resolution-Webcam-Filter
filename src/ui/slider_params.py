from typing import TypedDict

class ParamMeta(TypedDict):
    default: float
    min: float
    max: float
    float: bool
    category: str

PARAMS: dict[str, ParamMeta] = {
    "saturation": {"default": 0.6, "min": 0.2, "max": 1.5, "float": True, "category": "Color"},
    "green_gain": {"default": 1.03, "min": 0.8, "max": 1.2, "float": True, "category": "Color"},
    "red_gain": {"default": 0.92, "min": 0.8, "max": 1.2, "float": True, "category": "Color"},

    "blur_x": {"default": 6, "min": 1, "max": 21, "float": False, "category": "Lens"},
    "chromatic_shift": {"default": 1, "min": 0, "max": 3, "float": False, "category": "Lens"},
    
    "contrast": {"default": 0.85, "min": 0.5, "max": 1.5, "float": True, "category": "Image"},
    "brightness": {"default": 0.08, "min": -0.2, "max": 0.2, "float": True, "category": "Image"},

    "noise_strength": {"default": 0.01, "min": 0.0, "max": 0.05, "float": True, "category": "Noise"},
    "noise_fine": {"default": 0.003, "min": 0.0, "max": 0.01, "float": True, "category": "Noise"},
    "noise_alpha": {"default": 0.9, "min": 0.7, "max": 0.99, "float": True, "category": "Noise"},
}