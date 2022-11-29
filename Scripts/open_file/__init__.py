import os

import easygui

from .mc import handle_mc
from .mcz import handle_mcz
from .mtmlinfo import handle_mtmlinfo
from .mtmlproj import handle_mtmlproj
from .mtmlz import handle_mtmlz


def main() -> None:
    """
    打开文件
    """
    if file_path := easygui.fileopenbox('打开文件'):
        file_ext = os.path.splitext(file_path)[1]

        if file_ext == '.mtmlproj':
            handle_mtmlproj(file_path)

        elif file_ext == '.mtmlinfo':
            handle_mtmlinfo(file_path)

        elif file_ext == '.mtmlz':
            handle_mtmlz(file_path)

        elif file_ext == '.mc':
            handle_mc(file_path)

        elif file_ext == '.mcz':
            handle_mcz(file_path)

        else:
            easygui.msgbox(f'暂不支持打开 {file_ext.strip(".")} 文件。', '打开文件', '好的')
