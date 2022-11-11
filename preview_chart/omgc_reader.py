import hashlib
import struct

import easygui

from constants import *

from .common import *


def read_omgc(omgc_path: str, omgc_md5: str) -> tuple:
    """
    读取 omgc 谱面文件
    """

    chart_data = open(omgc_path, 'rb').read()
    if hashlib.md5(chart_data).hexdigest() != omgc_md5:
        easygui.msgbox('谱面文件 MD5 不匹配，可能已被篡改！', '无法打开谱面', '返回')

    def read_4byte():
        """
        从 omgc 文件读取 4 字节（一个数据）
        """
        index = 0
        while True:
            yield chart_data[index:index+4]
            index += 4
    read_4byte = read_4byte()

    # 文件开头 4 字节必须是“omgc”的 ASCII 码
    if next(read_4byte).decode('ascii') != 'omgc':
        easygui.msgbox('谱面文件头不符合 omgc 格式！', '无法打开谱面', '返回')
        return None

    def read_data(data_type):
        """
        读取一个指定类型的数据
        """
        return struct.unpack(OMGC_STRUCT_FORMAT[data_type], next(read_4byte))[0]

    def read_multi_data(*args):
        """
        读取多个指定类型的数据
        """
        return list(map(read_data, args))

    omgc_version = read_data(int)
    if omgc_version not in PREVIEW_SUPPORTED_OMGC_VERSIONS:
        if not easygui.ynbox(f'暂不支持此版本（{omgc_version}）的 omgc 文件！\n目前支持的版本为：{PREVIEW_SUPPORTED_OMGC_VERSIONS}\n是否强行打开谱面？', '打开谱面受阻', ('继续', '返回')):
            return None

    line_count, note_count, cmd_count = read_multi_data(int, int, int)

    lines = []
    for i in range(line_count):
        lines.append(Line(*read_multi_data(float, float, float)))

    notes = []
    activated_notes = [[]]*PREVIEW_TRACK_NUMBER
    for i in range(note_count):
        note_data = read_multi_data(float, float, int, float, float, float, int, int, int)
        if note_data.pop():
            activated_notes[note_data[2]].append(i)
        notes.append(Note(*note_data))

    commands = []
    for i in range(cmd_count):
        cmd_time, cmd_type, cmd_param_count = read_multi_data(float, int, int)
        if cmd_type in COMMAND_PARAM_TYPE:
            cmd_params = read_multi_data(*COMMAND_PARAM_TYPE[cmd_type])
            commands.append((cmd_time, cmd_type, cmd_params))
        else:
            # 跳过未知类型的指令
            for j in range(cmd_param_count):
                next(read_4byte)

    return lines, notes, commands, activated_notes
