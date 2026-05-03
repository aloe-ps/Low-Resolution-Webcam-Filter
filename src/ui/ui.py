import os
from PyQt5.QtWidgets import (
    QGroupBox, QInputDialog, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSlider, QPushButton, QListWidget
)
from PyQt5.QtCore import Qt

from content import TOOLTIPS
from setting.preset import PRESET_DIR, list_presets, load_preset, save_preset
from setting.stylesheet import load_stylesheet
from ui.slider_params import PARAMS
from collections import defaultdict


class ControlUI(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config

        self.setWindowTitle("Low Resolution Camera Filter")
        style_data = load_stylesheet("style.css")
        print("Loaded stylesheet:", "style.css" if style_data else "None")
        if style_data:
            self.setStyleSheet(style_data)
        self.setMinimumSize(800, 500)

        main = QHBoxLayout()
        self.setLayout(main)

        # --- 左：プリセット一覧
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

        main.addLayout(left, 1)

        # --- 右：スライダー
        self.sliders = {}
        right = QVBoxLayout()

        groups = defaultdict(list)

        for name, meta in PARAMS.items():
            groups[meta["category"]].append((name, meta))

        for category, items in groups.items():
            box, layout = self.create_group(category)

            for name, meta in items:
                self.add_slider(
                    layout,
                    name,
                    name,
                    meta["min"],
                    meta["max"],
                    meta["float"]
                )

            right.addWidget(box)
        main.addLayout(right, 2)


    def create_group(self, title):
        box = QGroupBox(title)

        layout = QVBoxLayout()
        box.setLayout(layout)
        return box, layout

    def add_slider(self, layout, label, attr, minv, maxv, float_mode=False):
        container = QVBoxLayout()

        # --- 上段（ラベル＋i）
        top = QHBoxLayout()

        lbl = QLabel()

        info = QLabel("ⓘ")
        info.setStyleSheet("color: #aaa; font-weight: bold;")

        # ツールチップ設定
        if attr in TOOLTIPS:
            info.setToolTip(TOOLTIPS[attr])

        top.addWidget(lbl)
        top.addWidget(info)
        top.addStretch()

        # --- スライダー
        slider = QSlider(Qt.Orientation.Horizontal)

        if float_mode:
            slider.setMinimum(int(minv * 100))
            slider.setMaximum(int(maxv * 100))
            slider.setValue(int(getattr(self.config, attr) * 100))
        else:
            slider.setMinimum(int(minv))
            slider.setMaximum(int(maxv))
            slider.setValue(int(getattr(self.config, attr)))

        def update(v):
            val = v / 100 if float_mode else v
            setattr(self.config, attr, val)
            lbl.setText(f"{label}: {val}")

        slider.valueChanged.connect(update)

        self.sliders[attr] = (slider, lbl, float_mode)

        update(slider.value())

        container.addLayout(top)
        container.addWidget(slider)
        layout.addLayout(container)

    def update_ui(self):
        for attr, (slider, lbl, float_mode) in self.sliders.items():
            val = getattr(self.config, attr)

            if float_mode:
                slider.setValue(int(val * 100))
            else:
                slider.setValue(int(val))

    # -- プリセット保存
    def save_current(self):
        name, ok = QInputDialog.getText(self, "Save", "Preset name:")
        if ok and name:
            save_preset(self.config, name)
            self.load_preset_list()

    # -- プリセット選択
    def select_preset(self, item):
        path = os.path.join(PRESET_DIR, item.text())
        load_preset(self.config, path)
        self.update_ui()

    # -- プリセット一覧更新
    def load_preset_list(self):
        self.preset_list.clear()
        for p in list_presets():
            self.preset_list.addItem(p)
        
    def closeEvent(self, event):
        os._exit(0)

    def reset_config(self):
        self.config.reset()
        self.update_ui()

        import filter
        filter.fixed_noise = None
        filter.prev_noise = None