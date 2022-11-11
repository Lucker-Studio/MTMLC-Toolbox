import tempfile
import zipfile

import easygui

from .game_launcher import launch


def main() -> None:
    file_path = easygui.fileopenbox('选择文件', '谱面预览', '*.omgz', ['*.omgz', '*.tpl', '*.mcz'])
    if file_path is None:
        return
    chart_dir = tempfile.mkdtemp()
    zipfile.ZipFile(file_path).extractall(chart_dir)
    launch(chart_dir)
