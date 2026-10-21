from PyQt5.QtWidgets import (
    QLabel, QPushButton, QListWidget, QVBoxLayout
)
from setting.preset import list_presets


class PresetPanelMixin:
    def build_preset_panel(self, parent_layout):
        left = QVBoxLayout()
        left.addWidget(QLabel("Presets"))

        self.preset_list = QListWidget()
        left.addWidget(self.preset_list)

        self.load_preset_list()
        self.preset_list.itemClicked.connect(self.select_preset)

        btn_save = QPushButton("Save Current")
        btn_save.clicked.connect(self.save_current)

        btn_reset = QPushButton("Reset to Default")
        btn_reset.clicked.connect(self.reset_config)

        left.addWidget(btn_save)
        left.addWidget(btn_reset)
        parent_layout.addLayout(left, 1)

    def load_preset_list(self):
        self.preset_list.clear()
        for preset_name in list_presets():
            self.preset_list.addItem(preset_name)

    def save_current(self):
        raise NotImplementedError

    def select_preset(self, item):
        raise NotImplementedError

    def reset_config(self):
        raise NotImplementedError
