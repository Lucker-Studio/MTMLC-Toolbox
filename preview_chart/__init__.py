import os
import tempfile

import easygui

from common import *
from export_chart.batcher import batch_project
from export_chart.converter import proj2chart
from export_chart.chart_writer import write_mtmlc
from import_chart.converter import mc2mtmlproj
from import_chart.dir_importer import import_dir

from .game_launcher import launch


def main() -> None:
    file_path = easygui.fileopenbox('选择文件', '预览谱面', '*.mtmlz', ['*.mtmlz', '*.mcz', '*.mc', '*.mtmlinfo'])
    if file_path is None:
        return
    file_dir, file_name = os.path.split(file_path)
    chart_ext = os.path.splitext(file_name)[1]
    chart_dir = tempfile.mkdtemp()
    if chart_ext == '.mtmlz':
        unpack_zip(file_path, chart_dir)
    elif chart_ext == '.mcz':
        unpack_zip(file_path, chart_dir)
        song_info = import_dir(chart_dir)
        files = batch_project(**song_info, dir_path=chart_dir)
        pack_dir(files, chart_dir)
    elif chart_ext == '.mc':
        mtmlc_path = os.path.join(chart_dir, chart_info['difficulty']+'.mtmlc')
        song_info, chart_info, project_data = mc2mtmlproj(read_json(file_path))
        lines, notes, commands = proj2chart(project_data)
        write_mtmlc(lines, notes, commands, mtmlc_path)
        song_info['music_file'] = os.path.join(file_dir, song_info['music_file'])
        if 'illustration_file' in song_info:
            song_info['illustration_file'] = os.path.join(file_dir, song_info['illustration_file'])
        else:
            song_info['illustration_file'] = os.path.join(RESOURCES_DIR, 'Default.jpg')
        song_info.setdefault('title', 'Untitled Song')
        song_info.setdefault('composer', 'Unknown')
        song_info.setdefault('illustrator', 'Unknown')
        song_info = {
            **song_info,
            'charts': [{**chart_info, 'md5': get_md5(mtmlc_path)}]
        }
        write_json(song_info, os.path.join(chart_dir, 'index.mtmlinfo'))
    elif chart_ext == '.mtmlinfo':
        song_info = read_json(file_path)
        files = batch_project(**song_info, dir_path=file_dir)
        pack_dir(files, chart_dir)
    else:
        easygui.msgbox('不支持此格式！', '预览谱面', '好的')
        return
    launch(chart_dir)
