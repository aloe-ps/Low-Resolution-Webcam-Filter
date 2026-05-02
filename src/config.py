import json
import os

class Config:
    def __init__(self):
        self.defaults = {
            "green_gain": 1.03,
            "red_gain": 0.92,
            "saturation": 0.6,
            "blur_x": 6,
            "contrast": 0.85,
            "brightness": 0.08,
            "noise_strength": 0.01,
            "noise_fine": 0.003,
            "noise_alpha": 0.9,
            "chromatic_shift": 1,
        }

        self.load_dict(self.defaults)

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if k != "defaults"}

    def load_dict(self, d):
        for k, v in d.items():
            setattr(self, k, v)

    # ★追加
    def reset(self):
        self.load_dict(self.defaults)

config = Config()

# preset
PRESET_DIR = "presets"
os.makedirs(PRESET_DIR, exist_ok=True)

def save_preset(config, name):
    path = os.path.join(PRESET_DIR, name + ".json")
    with open(path, "w") as f:
        json.dump(config.to_dict(), f, indent=4)


def load_preset(config, path):
    with open(path, "r") as f:
        data = json.load(f)
    config.load_dict(data)

def list_presets():
    return [f for f in os.listdir(PRESET_DIR) if f.endswith(".json")]

def load_stylesheet(file_path):
    """外部の.qss（CSS）ファイルを読み込むヘルパー関数"""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""