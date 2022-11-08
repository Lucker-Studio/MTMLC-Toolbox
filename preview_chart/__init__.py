import tempfile
import zipfile

import easygui

from .game_launcher import launch


def main() -> None:
    zip_path = easygui.fileopenbox('打开 zip 谱面', '谱面预览', '*.zip')
    if zip_path is None:
        return
    chart_dir = tempfile.mkdtemp()
    zipfile.ZipFile(zip_path).extractall(chart_dir)
    launch(chart_dir)
