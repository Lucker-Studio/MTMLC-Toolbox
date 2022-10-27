import hashlib
import os
import struct
import tempfile
import zipfile

import easygui
import pygame

from constants import *


def main():
    zip_path = easygui.fileopenbox('选择 ZIP 文件', '谱面预览', '*.zip')
    if zip_path is None:  # 关闭对话框
        return
    song_folder = tempfile.mkdtemp()
    zipfile.ZipFile(zip_path).extractall(song_folder)  # 解压文件到临时文件夹

    charts = {}  # 该歌曲谱面列表
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
        if chart_name is None:  # 关闭对话框
            return

        chart = charts[chart_name]
        chart_data = open(os.path.join(song_folder, 'charts', chart[0]+'.omgc'), 'rb').read()
        if hashlib.md5(chart_data).hexdigest() != chart[3]:  # 校验谱面 MD5
            easygui.msgbox('谱面文件已被篡改，无法预览！', '谱面预览', '好的')
            continue

        def data_reader_gen():  # 迭代器函数，每次读取一字节数据
            for i in chart_data:
                yield bytes(i)
        data_reader = data_reader_gen()

        def read_data(type_: type):  # 读取数据并解包为指定类型
            return struct.unpack({int: '>i', float: '>f'}[type_], next(data_reader))[0]

        cmd_list = []  # 谱面指令列表
        for i in range(read_data(int)):
            time = read_data(float)  # 指令执行时间（s）
            cmd_type = read_data(int)  # 指令类型
            param_cnt = read_data(int)  # 参数数量
            param_type = {
                ADD_NOTE: (int, int, float, float, float, int, int, float, float, float),
                CHANGE_NOTE_POS: (int, float, float, float),
                CHANGE_NOTE_TRACK: (int, int, *((param_cnt-2)*(float,))),
                ACTIVATE_NOTE: (int,),
                CHANGE_LINE_POS: (int, *((param_cnt-1)*(float,)))
            }.get(cmd_type)  # 指令参数类型
            if param_type is None:  # 未知指令
                for i in range(param_cnt):  # 跳过一定数量的参数
                    next(data_reader)
                continue
            params = map(read_data, param_type)  # 批量读取参数
            cmd_list.append((time, cmd_type, params))
