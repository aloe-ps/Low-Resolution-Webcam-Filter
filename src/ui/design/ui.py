import os
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QInputDialog
from setting.preset import PRESET_DIR, load_preset, save_preset
from setting.stylesheet import load_stylesheet
from ui.design.preset_panel import PresetPanelMixin
from ui.design.sliders import SliderPanelMixin


class ControlUI(QWidget, PresetPanelMixin, SliderPanelMixin):
    def __init__(self, config):
        super().__init__()
        self.config = config

        self.setWindowTitle("Low Resolution Camera Filter")
        style_data = load_stylesheet("style.css")
        print("Loaded stylesheet:", "style.css" if style_data else "None")
        if style_data:
            self.setStyleSheet(style_data)
        self.setMinimumSize(800, 500)

        self.main = QHBoxLayout()
        self.setLayout(self.main)

        self.build_preset_panel(self.main)
        self.build_slider_panel(self.main)

    def save_current(self):
        name, ok = QInputDialog.getText(self, "Save", "Preset name:")
        if ok and name:
            save_preset(self.config, name)
            self.load_preset_list()

    def select_preset(self, item):
        path = os.path.join(PRESET_DIR, item.text())
        load_preset(self.config, path)
        self.update_ui()

    def closeEvent(self, event):
        os._exit(0)

    def reset_config(self):
        self.config.reset()
        self.update_ui()

        import filter
        filter.fixed_noise = None
        filter.prev_noise = None
