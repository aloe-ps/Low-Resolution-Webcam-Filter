class Config:
    # annotations
    green_gain: float
    red_gain: float
    saturation: float
    blur_x: int
    contrast: float
    brightness: float
    noise_strength: float
    noise_fine: float
    noise_alpha: float
    chromatic_shift: int

    # default settings
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

    def reset(self):
        self.load_dict(self.defaults)

config = Config()