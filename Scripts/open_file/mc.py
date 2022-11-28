import os
import tempfile

import easygui

from Core.chart_compiler import compile_chart
from Core.chart_previewer import preview_chart
from Core.common import RESOURCES_PATH
from Core.file_io import get_md5, read_json, write_json
from Core.malody_importer import mc2mtmlproj
from Core.file_io import write_mtmlc


def convert_mc(file_path: str) -> None:
    """
    将 mc 文件转为 mtmlproj 文件
    """
    target = os.path.splitext(file_path)[0]+'.mtmlproj'
    mc_data = read_json(file_path)
    project_data = mc2mtmlproj(mc_data)[-1]
    write_json(project_data, target)


def handle_mc(file_path: str) -> None:
    """
    处理 mc 文件
    """
    if choice := easygui.buttonbox('请选择要对此文件执行的操作', file_path, ('预览谱面', '转换为 mtmlproj')):
        if choice == '预览谱面':
            chart_dir = tempfile.mkdtemp()
            song_info, chart_info, project_data = mc2mtmlproj(read_json(file_path))
            mtmlc_path = os.path.join(chart_dir, chart_info['difficulty']+'.mtmlc')
            lines, notes, commands = compile_chart(project_data)
            write_mtmlc(lines, notes, commands, mtmlc_path)
            song_info['music_file'] = os.path.join(os.path.split(file_path)[0], song_info['music_file'])
            if 'illustration_file' in song_info:
                song_info['illustration_file'] = os.path.join(os.path.split(file_path)[0], song_info['illustration_file'])
            else:
                song_info['illustration_file'] = os.path.join(RESOURCES_PATH, 'Default.jpg')
            song_info.setdefault('title', 'Untitled Song')
            song_info.setdefault('composer', 'Unknown')
            song_info.setdefault('illustrator', 'Unknown')
            song_info = {
                **song_info,
                'charts': [{**chart_info, 'md5': get_md5(mtmlc_path)}]
            }
            write_json(song_info, os.path.join(chart_dir, 'index.mtmlinfo'))
            preview_chart(chart_dir)

        elif choice == '转换为 mtmlproj':
            convert_mc(file_path)
            easygui.msgbox('转换成功！', '转换为 mtmlproj', '好的')
