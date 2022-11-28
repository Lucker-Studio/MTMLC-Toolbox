import os
import tempfile
import traceback

import easygui

from Core.chart_previewer import preview_chart
from Core.file_io import pack_folder
from Core.folder_importer import import_folder
from Core.project_exporter import export_project
from Scripts.open_file.mc import convert_mc
from Scripts.open_file.mcz import convert_mcz, import_mcz

from .open_file.mtmlinfo import export_mtmlinfo, preview_mtmlinfo


def batch_files(folder_path: str, file_type: str, title: str, operation) -> None:
    """
    对文件夹内所有某种类型的文件执行指定操作并反馈结果。
    """
    success = []
    failure = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(file_type):
            try:
                operation(os.path.join(folder_path, file_name))
                success.append(file_name)
            except Exception:
                traceback.print_exc()
                failure.append(file_name)
    msg = ''
    if success:
        msg += f'{len(success)}个文件成功：\n'
        for i in success:
            msg += i+'\n'
    if failure:
        msg += f'{len(failure)}个文件失败：\n'
        for i in failure:
            msg += i+'\n'
    easygui.msgbox(msg, title, '好的')


def open_folder() -> None:
    """
    打开文件夹
    """
    if folder_path := easygui.diropenbox('打开文件夹'):
        ls = os.listdir(folder_path)
        op = []
        if 'index.mtmlinfo' in ls:
            op.append('通过 index.mtmlinfo 预览谱面')
            op.append('通过 index.mtmlinfo 导出 mtmlz')
        if [i for i in ls if i.endswith('.mc')]:
            op.append('通过 mc 文件预览谱面')
            op.append('将所有 mc 转换为 mtmlproj')
        if [i for i in ls if i.endswith('.mcz')]:
            op.append('将所有 mcz 导入为工程文件夹')
            op.append('将所有 mcz 转换为 mtmlz')
        if not op:
            easygui.msgbox(f'没有可对此文件夹执行的操作。', '打开文件夹', '好的')
        elif choice := easygui.choicebox('请选择要对此文件夹执行的操作', folder_path, op):
            if choice == '通过 index.mtmlinfo 预览谱面':
                preview_mtmlinfo(os.path.join(folder_path, 'index.mtmlinfo'))
            elif choice == '通过 index.mtmlinfo 导出 mtmlz':
                export_mtmlinfo(os.path.join(folder_path, 'index.mtmlinfo'))
            elif choice == '通过 mc 文件预览谱面':
                song_info = import_folder(folder_path)
                files = export_project(**song_info, folder_path=folder_path)
                chart_dir = tempfile.mkdtemp()
                pack_folder(files, chart_dir)
                preview_chart(chart_dir)
            elif choice == '将所有 mc 转换为 mtmlproj':
                batch_files(folder_path, '.mc', '将所有 mc 转换为 mtmlproj', convert_mc)
            elif choice == '将所有 mcz 导入为工程文件夹':
                batch_files(folder_path, '.mcz', '将所有 mcz 导入为工程文件夹', import_mcz)
            elif choice == '将所有 mcz 转换为 mtmlz':
                batch_files(folder_path, '.mcz', '将所有 mcz 转换为 mtmlz', convert_mcz)
