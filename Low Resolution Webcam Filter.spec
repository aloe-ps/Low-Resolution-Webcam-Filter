# -*- mode: python ; coding: utf-8 -*-


_QT_PLUGIN_DIRS = {
    "assetimporters",
    "audio",
    "bearer",
    "generic",
    "geoservices",
    "iconengines",
    "imageformats",
    "mediaservice",
    "platformthemes",
    "playlistformats",
    "position",
    "renderers",
    "sceneparsers",
    "sensorgestures",
    "sensors",
    "sqldrivers",
    "texttospeech",
    "webview",
}

_QT_UNUSED_BINARIES = {
    "d3dcompiler_47.dll",
    "libegl.dll",
    "libglesv2.dll",
    "opengl32sw.dll",
    "qt5dbus.dll",
    "qt5network.dll",
    "qt5qml.dll",
    "qt5qmlmodels.dll",
    "qt5quick.dll",
    "qt5quickwidgets.dll",
    "qt5svg.dll",
    "qt5websockets.dll",
    "qt5xml.dll",
    "qt5xmlpatterns.dll",
}


def _is_unused_qt(entry):
    name = str(entry[0]).replace("\\", "/").lower()

    if name.startswith("pyqt5/qt5/translations/"):
        return True

    if name.startswith("pyqt5/qt5/plugins/"):
        parts = name.split("/")
        if len(parts) >= 4:
            plugin = parts[3]
            if plugin == "platforms":
                return not name.endswith("/qwindows.dll")
            if plugin in _QT_PLUGIN_DIRS:
                return True

    if name.startswith("pyqt5/qt5/bin/"):
        return name.rsplit("/", 1)[-1] in _QT_UNUSED_BINARIES

    return False


a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('style.css', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'numpy.testing',
        'numpy.f2py',
        'numpy.distutils',
        'numpy._core._multiarray_tests',
        'PyQt5.QtDesigner',
        'PyQt5.QtHelp',
        'PyQt5.QtMultimedia',
        'PyQt5.QtNetwork',
        'PyQt5.QtOpenGL',
        'PyQt5.QtPrintSupport',
        'PyQt5.QtQml',
        'PyQt5.QtQuick',
        'PyQt5.QtSql',
        'PyQt5.QtSvg',
        'PyQt5.QtTest',
        'PyQt5.QtWebSockets',
        'PyQt5.QtXml',
        'PyQt5.QtXmlPatterns',
        'PyQt5.uic',
    ],
    noarchive=False,
    optimize=2,
)
a.binaries = [entry for entry in a.binaries if not _is_unused_qt(entry)]
a.datas = [entry for entry in a.datas if not _is_unused_qt(entry)]

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Low Resolution Webcam Filter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
