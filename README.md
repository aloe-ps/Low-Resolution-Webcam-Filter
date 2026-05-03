# Low Resolution Webcam Filter

## Overview

This project provides a real-time webcam filter that simulates the look of low-resolution consumer webcams (e.g., early Logitech devices) while keeping the original resolution intact.
It applies color shifts, blur, noise, and subtle optical artifacts to reproduce a characteristic “cheap webcam” appearance.

The processed video can be routed through a virtual camera and recorded in OBS or used in other applications.

---

## Features

* Real-time webcam processing
* Virtual camera output (compatible with OBS)
* Adjustable parameters via GUI (PyQt)
* Preset system (save/load JSON)
* Preset list with one-click switching
* Reset to default settings
* Tooltip descriptions for each parameter
* Categorized controls (Color / Lens / Noise)

---

## Project Structure

```
src/
├─ main.py          # Entry point
├─ filter.py        # Image processing logic
├─ ui.py            # PyQt UI
├─ config.py        # Parameter + preset management
├─ content.py       # Tooltips content
```

---

## Requirements

* Python 3.9+
* uv
* OpenCV
* NumPy
* PyQt5
* pyvirtualcam

---

## Usage
Run the application:
```
git clone https://github.com/aloe-ps/Low-resolution-Filter.git
cd Low-resolution-Filter
uv run src\main.py
```
## Build
### Windows
```
uv add -r requirements-build.txt
pyinstaller --name "Low Resolution Webcam Filter" --noconsole --onefile --add-data "style.css;." src\main.py
```
### Mac / Linux
```
uv add -r requirements-build.txt
pyinstaller --name "Low Resolution Webcam Filter" --noconsole --onefile --add-data "style.css:." src\main.py
```

* The UI window will open.
* The camera feed will start automatically.
* The processed output is sent to a virtual camera.
* Select the virtual camera in OBS or other software.

---

## Controls

### Presets

* Presets are stored in the `presets/` folder.
* Click a preset to apply it.
* Use “Save Current” to create a new preset.
* Use “Reset to Default” to restore initial values.

### Parameters

#### Color

* Saturation: Controls color intensity
* Green Gain: Adjusts green channel bias
* Red Gain: Adjusts red channel bias

#### Lens

* Blur X: Horizontal blur amount
* Chromatic Shift: Simulates color misalignment

#### Noise

* Noise Strength: Base noise intensity
* Noise Fine: Fine-grain noise level
* Noise Alpha: Temporal stability of noise

Hover over the info icon next to each control for a description.

---

## Notes

* The UI runs on the main thread; camera processing runs in a background thread.
* Closing the UI window terminates the entire application.
* Presets are simple JSON files and can be edited manually.

---

## License

This project is licensed under MIT License
