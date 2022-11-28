import os
import tempfile

import easygui

from Core.chart_previewer import preview_chart
from Core.file_io import pack_folder, pack_zip, save_file, unpack_zip
from Core.folder_importer import import_folder
from Core.project_exporter import export_project


def import_mcz(file_path: str) -> None:
    """
    将 mcz 文件导入为工程文件夹
    """
    target = os.path.splitext(file_path)[0]
    unpack_zip(file_path, target)
    import_folder(target)


def convert_mcz(file_path: str) -> None:
    """
    将 mcz 文件转换为 mtmlz
    """
    target = tempfile.mkdtemp()
    unpack_zip(file_path, target)
    song_info = import_folder(target)
    files = export_project(**song_info, folder_path=target)
    pack_zip(files, os.path.splitext(file_path)[0]+'.mtmlz')


def handle_mcz(file_path: str) -> None:
    """
    处理 mcz 文件
    """
    if choice := easygui.buttonbox('请选择要对此文件执行的操作', file_path, ('预览谱面', '导入为工程文件夹', '转换为 mtmlz')):
        if choice == '预览谱面':
            chart_dir = tempfile.mkdtemp()
            unpack_zip(file_path, chart_dir)
            song_info = import_folder(chart_dir)
            files = export_project(**song_info, folder_path=chart_dir)
            pack_folder(files, chart_dir)
            preview_chart(chart_dir)

        elif choice == '导入为工程文件夹':
            import_mcz(file_path)
            easygui.msgbox('导入成功！', '导入为工程文件夹', '好的')

        elif choice == '转换为 mtmlz':
            convert_mcz(file_path)
            easygui.msgbox('转换成功！', '转换为 mtmlz', '好的')
