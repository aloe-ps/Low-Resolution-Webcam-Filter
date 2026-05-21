from typing import TypedDict

class ParamMeta(TypedDict):
    default: float
    min: float
    max: float
    float: bool
    category: str
    tooltip: str

PARAMS: dict[str, ParamMeta] = {
    "saturation": {"default": 0.6, "min": 0.2, "max": 1.5, "float": True, "category": "Color","tooltip":"色の鮮やかさ。低いほどくすむ"},
    "green_gain": {"default": 1.03, "min": 0.8, "max": 1.2, "float": True, "category": "Color","tooltip":"緑の強さ"},
    "red_gain": {"default": 0.92, "min": 0.8, "max": 1.2, "float": True, "category": "Color","tooltip":"赤の強さ"},
    "blue_gain": {"default": 1, "min": 0.8, "max": 1.2, "float": True, "category": "Color","tooltip":"青の強さ"},
    "temperature": {"default": 0.0, "min": -1.0, "max": 1.0, "float": True, "category": "Color","tooltip":"色温度"},

    "blur_x": {"default": 6, "min": 1, "max": 21, "float": False, "category": "Lens","tooltip":"横方向のぼかし量。大きいほどにじむ"},
    "chromatic_shift": {"default": 1, "min": 0, "max": 3, "float": False, "category": "Lens","tooltip":"色収差"},
    
    "contrast": {"default": 0.85, "min": 0.5, "max": 1.5, "float": True, "category": "Image","tooltip":"コントラスト"},
    "brightness": {"default": 0.08, "min": -0.2, "max": 0.2, "float": True, "category": "Image","tooltip":"明るさ"},

    "noise_strength": {"default": 0.01, "min": 0.0, "max": 0.05, "float": True, "category": "Noise","tooltip":"ノイズの強さ"},
    "noise_fine": {"default": 0.003, "min": 0.0, "max": 0.01, "float": True, "category": "Noise","tooltip":"細かいノイズ"},
    "noise_alpha": {"default": 0.9, "min": 0.7, "max": 0.99, "float": True, "category": "Noise","tooltip":"ノイズの透明度"},
}