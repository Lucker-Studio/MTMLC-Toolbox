import json
import os
import tempfile
import zipfile

import easygui

from export_chart.batcher import batch_charts
from export_chart.packer import pack_to_dir
from import_chart.mcz_unpacker import unpack_mcz

from .game_launcher import launch


def main() -> None:
    file_path = easygui.fileopenbox('选择文件', '预览谱面', '*.omgz', ['*.omgz', '*.tpl', '*.mcz'])
    if file_path is None:
        return
    chart_ext = os.path.splitext(file_path)[1]
    chart_dir = tempfile.mkdtemp()
    if chart_ext == '.omgz':
        zipfile.ZipFile(file_path).extractall(chart_dir)
    elif chart_ext == '.tpl':
        template_data = json.load(open(file_path, encoding='utf-8'))
        music_path, illustration_path, title, composer, illustrator, charts = template_data
        files = batch_charts(title, composer, illustrator, music_path, illustration_path, charts)
        pack_to_dir(files, chart_dir)
    elif chart_ext == '.mcz':
        info = unpack_mcz(file_path, chart_dir)
        files = batch_charts(**info)
        pack_to_dir(files, chart_dir)
    else:
        easygui.msgbox('不支持此格式！', '预览谱面', '好的')
        return
    launch(chart_dir)
