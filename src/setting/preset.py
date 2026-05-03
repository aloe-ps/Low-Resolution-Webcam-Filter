# preset
import json
import os

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