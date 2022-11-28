import os

import easygui

from .handle_mc import handle_mc
from .handle_mcz import handle_mcz
from .handle_mtmlinfo import handle_mtmlinfo
from .handle_mtmlz import handle_mtmlz


def open_file() -> None:
    """
    打开文件
    """
    if file_path := easygui.fileopenbox('打开文件'):
        file_dir, file_name = os.path.split(file_path)
        file_ext = os.path.splitext(file_name)[1]

        if file_ext == '.mtmlproj':
            easygui.msgbox('暂不支持打开 mtmlproj 文件，如需使用相关功能，请打开 mtmlinfo 文件。', '打开文件', '好的')

        elif file_ext == '.mtmlinfo':
            handle_mtmlinfo(file_path)

        elif file_ext == '.mtmlc':
            easygui.msgbox('暂不支持打开 mtmlc 文件，如需使用相关功能，请打开 mtmlz 文件。', '打开文件', '好的')

        elif file_ext == '.mtmlz':
            handle_mtmlz(file_path)

        elif file_ext == '.mc':
            handle_mc(file_path)

        elif file_ext == '.mcz':
            handle_mcz(file_path)

        else:
            easygui.msgbox(f'暂不支持打开 {file_ext.strip(".")} 文件。', '打开文件', '好的')
