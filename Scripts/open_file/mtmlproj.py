import os

import easygui

from Core.chart_compiler import compile_chart
from Core.file_io import read_json, write_mtmlc


def handle_mtmlproj(file_path: str) -> None:
    """
    处理 mtmlproj 文件
    """
    if choice := easygui.buttonbox('请选择要对此文件执行的操作', file_path, ('编译为 mtmlc',)):
        if choice == '编译为 mtmlc':
            project_data = read_json(file_path)
            mtmlc_path = os.path.splitext(file_path)[0]+'.mtmlc'
            lines, notes, commands = compile_chart(project_data)
            write_mtmlc(lines, notes, commands, mtmlc_path)
            easygui.msgbox('编译成功！', '编译为 mtmlc', '好的')
