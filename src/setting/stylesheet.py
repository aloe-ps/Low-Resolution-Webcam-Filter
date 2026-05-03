import os
import sys

def get_stylesheet(filename):
    """
    指定されたcssファイルを読み込みます
    exeファイルに埋め込まれているファイルを基本的に使用し、同じディレクトリにファイルがあればそちらを使用します
    """
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    external_path = os.path.join(base_path, filename)

    if os.path.exists(external_path):
        return external_path

    bundle_dir = getattr(sys, '_MEIPASS', base_path)
    return os.path.join(bundle_dir, filename)

def load_stylesheet(filename):
    css_path = get_stylesheet(filename)
    with open(css_path, "r", encoding="utf-8") as f:
        return f.read()