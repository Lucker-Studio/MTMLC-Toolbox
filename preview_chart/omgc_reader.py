import hashlib
import math
import struct

import easygui
from constants import *


class Linear_func:
    """
    线性缓动函数（val=kt+b)。
    """

    def __init__(self, k: float, b: float) -> None:
        self.k = k
        self.b = b

    def value(self, t: float) -> float:
        return self.k*t+self.b


class Sine_func:
    """
    正弦缓动函数（val=Asin(wt+φ)+b）。
    """

    def __init__(self, A: float, o: float, p: float, b: float) -> None:
        self.A = A
        self.o = o
        self.p = p
        self.b = b

    def value(self, t: float) -> float:
        return self.A*math.sin(self.o*t+self.p)+self.b


class Line:
    """
    判定线。
    """

    def __init__(self, initial_position: float, initial_alpha: float) -> None:
        self.position_func = Linear_func(0, initial_position)
        self.alpha_func = Linear_func(0, initial_alpha)


def read_omgc(omgc_path: str, omgc_md5) -> tuple:
    """
    读取 omgc 谱面文件。
    """

    chart_data = open(omgc_path, 'rb').read()
    if hashlib.md5(chart_data).hexdigest() != omgc_md5:
        easygui.msgbox('谱面文件 MD5 不匹配，可能已被篡改！', '无法打开谱面', '返回')

    def read_4byte():
        index = 0
        while True:
            yield chart_data[index:index+4]
            index += 4
    read_4byte = read_4byte()

    if next(read_4byte).decode('ascii') != 'omgc':
        easygui.msgbox('谱面文件头不符合 omgc 格式！', '无法打开谱面', '返回')
        return None

    def read_data(data_type):
        return struct.unpack(STRUCT_FORMAT[data_type], next(read_4byte))[0]

    omgc_version = read_data(int)
    if omgc_version not in SUPPORTED_OMGC_VERSIONS:
        easygui.msgbox(f'不支持此版本（{omgc_version}）的 omgc 文件！\n目前支持的版本为：{SUPPORTED_OMGC_VERSIONS}', '无法打开谱面', '返回')
        return None

    line_size = read_data(int)
    line_count = read_data(int)
    note_size = read_data(int)
    note_count = read_data(int)
    cmd_size = read_data(int)
    cmd_count = read_data(int)
