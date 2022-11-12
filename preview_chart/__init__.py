import hashlib
import json
import os
import tempfile
import zipfile

import easygui

from constants import *
from export_chart.batcher import batch_charts
from export_chart.converter import omg2omgc
from export_chart.omgc_writer import write_omgc
from export_chart.packer import pack_to_dir
from import_chart.converter import malody2omegar
from import_chart.dir_importer import import_dir
from import_chart.mc_reader import read_mc

from .game_launcher import launch


def main() -> None:
    file_path = easygui.fileopenbox('选择文件', '预览谱面', '*.omgz', ['*.omgz', '*.omg', '*.mcz', '*.mc', '*.json'])
    if file_path is None:
        return
    file_dir, file_name = os.path.split(file_path)
    chart_name, chart_ext = os.path.splitext(file_name)
    chart_dir = tempfile.mkdtemp()
    if chart_ext == '.omgz':
        zipfile.ZipFile(file_path).extractall(chart_dir)
    elif chart_ext == '.omg':
        omgc_path = os.path.join(chart_dir, 'Default.omgc')
        project_data = json.load(open(file_path, encoding='utf-8'))
        lines, notes, commands = omg2omgc(project_data)
        write_omgc(lines, notes, commands, omgc_path)
        info = {
            'title': chart_name,
            'music_file': os.path.join(file_dir, project_data['music_file']),  # 预览时 os.path.join(A, B) 两个绝对路径只保留后一个
            'illustration_file': project_data['illustration_file'],
            'charts': [{
                'difficulty': 'Default',
                'number': '0',
                'writer': 'unknown',
                'md5': hashlib.md5(open(omgc_path, 'rb').read()).hexdigest()
            }]
        }
        if not info['illustration_file']:
            info['illustration_file'] = os.path.join(RESOURCES_DIR, 'Default.jpg')
        else:
            info['illustration_file'] = os.path.join(file_dir, info['illustration_file'])
        json.dump(info, open(os.path.join(chart_dir, 'info.json'), 'w', encoding='utf-8'))
    elif chart_ext == '.mcz':
        zipfile.ZipFile(file_path).extractall(chart_dir)
        info = import_dir(chart_dir)
        files = batch_charts(**info)
        pack_to_dir(files, chart_dir)
    elif chart_ext == '.mc':
        mc_data, chart_info, song_info = read_mc(file_path)
        omgc_path = os.path.join(chart_dir, chart_info['difficulty']+'.omgc')
        project_data = malody2omegar(mc_data)
        lines, notes, commands = omg2omgc(project_data)
        write_omgc(lines, notes, commands, omgc_path)
        info = {
            **song_info,
            'music_file': os.path.join(file_dir, project_data['music_file']),  # 预览时 os.path.join(A, B) 两个绝对路径只保留后一个
            'illustration_file': project_data['illustration_file'],
            'charts': [{**chart_info, 'md5': hashlib.md5(open(omgc_path, 'rb').read()).hexdigest()}]
        }
        if not info['illustration_file']:
            info['illustration_file'] = os.path.join(RESOURCES_DIR, 'Default.jpg')
        else:
            info['illustration_file'] = os.path.join(file_dir, info['illustration_file'])
        json.dump(info, open(os.path.join(chart_dir, 'info.json'), 'w', encoding='utf-8'))
    elif chart_ext == '.json':
        info = json.load(open(file_path, encoding='utf-8'))
        files = batch_charts(**info)
        pack_to_dir(files, chart_dir)
    else:
        easygui.msgbox('不支持此格式！', '预览谱面', '好的')
        return
    launch(chart_dir)
