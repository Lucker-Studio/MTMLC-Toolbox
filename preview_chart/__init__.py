import tempfile
import zipfile

import easygui


def main() -> None:
    zip_path = easygui.fileopenbox('打开 zip 谱面', '谱面预览', '*.zip')
    if zip_path is None:
        return
    zip_dir = tempfile.mkdtemp()
    zipfile.ZipFile(zip_path).extractall(zip_dir)
    