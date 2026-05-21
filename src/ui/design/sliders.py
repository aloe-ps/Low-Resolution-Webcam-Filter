from collections import defaultdict
from typing import Any
from PyQt5.QtWidgets import (
    QGroupBox, QLabel, QSlider,
    QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt
from ui.slider_params import PARAMS

class SliderPanelMixin:
    config: Any

    def build_slider_panel(self, parent_layout):
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
                    meta["float"],
                    meta.get("tooltip", "")
                )

            right.addWidget(box)

        parent_layout.addLayout(right, 2)

    def create_group(self, title):
        box = QGroupBox(title)
        layout = QVBoxLayout()
        box.setLayout(layout)
        return box, layout

    def add_slider(self, layout, label, attr, minv, maxv, float_mode=False, tooltip=""):
        container = QVBoxLayout()

        top = QHBoxLayout()
        lbl = QLabel()

        info = QLabel("ⓘ")
        info.setStyleSheet("color: #aaa; font-weight: bold;")

        if tooltip:
            info.setToolTip(tooltip)

        top.addWidget(lbl)
        top.addWidget(info)
        top.addStretch()

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