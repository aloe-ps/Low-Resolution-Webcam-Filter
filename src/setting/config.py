from ui.slider_params import PARAMS

class Config:
    green_gain: float
    red_gain: float
    blue_gain: float
    saturation: float
    temperature: float
    blur_x: int
    contrast: float
    brightness: float
    noise_strength: float
    noise_fine: float
    noise_alpha: float
    chromatic_shift: int

    def __init__(self):
        self.reset()

    def reset(self) -> None:
        for name, meta in PARAMS.items():
            # assert hasattr(self, name)
            setattr(self, name, meta["default"])

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if k != "defaults"}

    def load_dict(self, d):
        for k, v in d.items():
            setattr(self, k, v)

config = Config()