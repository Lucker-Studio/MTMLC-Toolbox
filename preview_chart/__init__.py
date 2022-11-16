import hashlib
import json
import os
import tempfile

import easygui

from constants import *
from export_chart.batcher import batch_charts
from export_chart.converter import omg2omgc
from export_chart.omgc_writer import write_omgc
from export_chart.packer import pack_to_dir
from import_chart.converter import malody2omegar
from import_chart.dir_importer import import_dir
from zip_unpacker import unpack_zip

from .game_launcher import launch


def main() -> None:
    file_path = easygui.fileopenbox('选择文件', '预览谱面', '*.omgz', ['*.omgz', '*.mcz', '*.mc', '*.json'])
    if file_path is None:
        return
    file_dir, file_name = os.path.split(file_path)
    chart_name, chart_ext = os.path.splitext(file_name)
    chart_dir = tempfile.mkdtemp()
    if chart_ext == '.omgz':
        unpack_zip(file_path, chart_dir)
    elif chart_ext == '.mcz':
        unpack_zip(file_path, chart_dir)
        song_info = import_dir(chart_dir)
        files = batch_charts(**song_info)
        pack_to_dir(files, chart_dir)
    elif chart_ext == '.mc':
        omgc_path = os.path.join(chart_dir, chart_info['difficulty']+'.omgc')
        song_info, chart_info, project_data = malody2omegar(json.load(open(file_path, encoding='utf-8')))
        lines, notes, commands = omg2omgc(project_data)
        write_omgc(lines, notes, commands, omgc_path)
        song_info.setdefault('title', 'Untitled Song')
        song_info.setdefault('composer', 'Unknown')
        song_info.setdefault('illustration_file', os.path.join(RESOURCES_DIR, 'Default.jpg'))
        song_info = {
            **song_info,
            'charts': [{**chart_info, 'md5': hashlib.md5(open(omgc_path, 'rb').read()).hexdigest()}]
        }
        json.dump(song_info, open(os.path.join(chart_dir, 'index.omginfo'), 'w', encoding='utf-8'))
    elif chart_ext == '.json':
        song_info = json.load(open(file_path, encoding='utf-8'))
        files = batch_charts(**song_info)
        pack_to_dir(files, chart_dir)
    else:
        easygui.msgbox('不支持此格式！', '预览谱面', '好的')
        return
    launch(chart_dir)
