import os
import tempfile

import easygui

from Core.chart_compiler import compile_chart
from Core.chart_previewer import preview_chart
from Core.file_io import pack_folder, read_json, write_mtmlc
from Core.project_exporter import export_project


def handle_mtmlproj(file_path: str) -> None:
    """
    处理 mtmlproj 文件
    """
    op = []
    file_dir = os.path.split(file_path)[0]
    if 'index.mtmlinfo' in os.listdir(file_dir):
        op.append('预览谱面')
    op.append('编译为 mtmlc（仅供测试）')
    if choice := easygui.buttonbox('请选择要对此文件执行的操作', file_path, op):
        if choice == '预览谱面':
            song_info = read_json(os.path.join(file_dir, 'index.mtmlinfo'))
            song_info['charts'] = [{'difficulty': 'Default', 'writer': 'Unknown', 'path': file_path}]
            files = export_project(**song_info, folder_path=os.path.split(file_path)[0])
            chart_dir = tempfile.mkdtemp()
            pack_folder(files, chart_dir)
            preview_chart(chart_dir)

        elif choice == '编译为 mtmlc（仅供测试）':
            project_data = read_json(file_path)
            mtmlc_path = os.path.splitext(file_path)[0]+'.mtmlc'
            lines, notes, commands = compile_chart(project_data)
            write_mtmlc(lines, notes, commands, mtmlc_path)
            easygui.msgbox('编译成功！', '编译为 mtmlc', '好的')
