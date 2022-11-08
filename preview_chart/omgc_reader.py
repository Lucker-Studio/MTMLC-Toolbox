import hashlib
import struct

import easygui
from constants import *

from .func import *


class Line:
    """
    判定线。
    """

    def __init__(self, initial_position: float, initial_alpha: float) -> None:
        # 线性函数，但是斜率为 0，那不就是常数吗~
        self.get_position = Linear_func(0, initial_position)
        self.get_alpha = Linear_func(0, initial_alpha)


class Note:
    """
    音符。
    """

    def __init__(self, properties: int, line: Line, initial_a: float, initial_b: float, initial_c: float, initial_showing_track: float, judging_track: int, start_time: float, end_time: float, showing_length: float) -> None:
        for i, property in enumerate(NOTE_PROPERTIES):
            # 把 note 的“属性”当作类的属性直接用
            self.__dict__[property] = bool(properties & 1 << i)
        self.line = line  # Python 对象作为引用参数传递，相当于指针
        self.get_relative_position = Quadratic_func(initial_a, initial_b, initial_c)
        self.get_showing_track = Linear_func(0, initial_showing_track)
        self.judging_track = judging_track
        self.start_time = start_time
        self.end_time = end_time
        self.showing_length = showing_length

    def get_position(self, t: float) -> float:
        """
        获取 note 的绝对位置。
        """
        # 绝对位置=判定线位置+相对位置*流速倍率
        return self.line.get_position(t)+self.get_relative_position(t)*PREVIEW_NOTE_SPEED_RATE


def read_omgc(omgc_path: str, omgc_md5: str) -> tuple:
    """
    读取 omgc 谱面文件。
    """

    chart_data = open(omgc_path, 'rb').read()
    if hashlib.md5(chart_data).hexdigest() != omgc_md5:
        easygui.msgbox('谱面文件 MD5 不匹配，可能已被篡改！', '无法打开谱面', '返回')

    def read_4byte():
        """
        从 omgc 文件读取 4 字节（一个数据）。
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
        读取一个指定类型的数据。
        """
        return struct.unpack(OMGC_STRUCT_FORMAT[data_type], next(read_4byte))[0]

    def read_multi_data(*args):
        """
        读取多个指定类型的数据。
        """
        return list(map(read_data, args))

    omgc_version = read_data(int)
    if omgc_version not in OMGC_SUPPORTED_VERSIONS:
        if not easygui.ynbox(f'暂不支持此版本（{omgc_version}）的 omgc 文件！\n目前支持的版本为：{OMGC_SUPPORTED_VERSIONS}\n是否强行打开谱面？', '打开谱面受阻', ('继续', '返回')):
            return None

    line_size, line_count, note_size, note_count, cmd_size, cmd_count = read_multi_data(*(int,)*6)

    lines = []
    for i in range(line_count):
        lines.append(Line(*read_multi_data(float, float)))

    notes = []
    for i in range(note_count):
        notes.append(Note(read_data(int), lines[read_data(int)], *read_multi_data(float, float, float, float, int, float, float, float)))

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

    return lines, notes, commands
