import hashlib
import os
import struct
import tempfile
import zipfile

import easygui
import pygame


def main():
    omgz_path = easygui.fileopenbox('选择 OMGZ 文件', '谱面预览', '*.omgz')
    if omgz_path is None:
        return
    song_folder = tempfile.mkdtemp()
    zipfile.ZipFile(omgz_path).extractall(song_folder)

    charts = {}
    with open(os.path.join(song_folder, 'info.txt'), encoding='utf-8') as f:
        title = f.readline()
        composer = f.readline()
        illustrator = f.readline()
        for i in range(int(f.readline())):
            difficulty = f.readline()
            diff_number = float(f.readline())
            writer = f.readline()
            md5 = f.readline()
            charts[f'{difficulty} {diff_number} By {writer}'] = (difficulty, diff_number, writer, md5)

    while True:
        chart_name = easygui.choicebox('请选择要预览的谱面', '谱面预览', charts.keys())
        if chart_name is None:
            return

        chart = charts[chart_name]
        chart_data = open(os.path.join(song_folder, 'charts', chart[0]+'.omgc'), 'rb').read()
        if hashlib.md5(chart_data).hexdigest() != chart[3]:
            easygui.msgbox('谱面文件已被篡改，无法预览！', '谱面预览', '好的')
            continue

        def data_reader_gen():
            for i in chart_data:
                yield bytes(i)
        data_reader = data_reader_gen()

        def read_data(type_: type):
            return struct.unpack({int: '>i', float: '>f'}[type_], next(data_reader))

        