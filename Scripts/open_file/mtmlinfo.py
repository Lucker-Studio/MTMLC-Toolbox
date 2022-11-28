import os
import tempfile

import easygui

from Core.chart_previewer import preview_chart
from Core.file_io import pack_folder, read_json, pack_zip, save_file
from Core.project_exporter import export_project


def preview_mtmlinfo(file_path: str) -> None:
    """
    通过 mtmlinfo 文件预览谱面
    """
    song_info = read_json(file_path)
    files = export_project(**song_info, folder_path=os.path.split(file_path)[0])
    chart_dir = tempfile.mkdtemp()
    pack_folder(files, chart_dir)
    preview_chart(chart_dir)


def export_mtmlinfo(file_path: str) -> None:
    """
    通过 mtmlinfo 文件导出 mtmlz
    """
    song_info = read_json(file_path)
    files = export_project(**song_info, folder_path=os.path.split(file_path)[0])
    if mtmlz_path := save_file('保存 mtmlz 文件', '.mtmlz', song_info['title']):
        pack_zip(files, mtmlz_path)
        easygui.msgbox('导出成功！', '导出 mtmlz', '好的')


def handle_mtmlinfo(file_path: str) -> None:
    """
    处理 mtmlinfo 文件
    """
    if choice := easygui.buttonbox('请选择要对此文件执行的操作', file_path, ('预览谱面', '导出 mtmlz')):
        if choice == '预览谱面':
            preview_mtmlinfo(file_path)
        elif choice == '导出 mtmlz':
            export_mtmlinfo(file_path)
