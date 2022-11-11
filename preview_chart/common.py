import math

from constants import *


class Linear_func:
    """
    线性函数（val=kt+b）
    """

    def __init__(self, k: float, b: float) -> None:
        self.k = k
        self.b = b

    def __call__(self, t: float) -> float:
        return self.k*t+self.b


class Sine_func:
    """
    正弦函数（val=Asin(wt+φ)+b）
    """

    def __init__(self, A: float, o: float, p: float, b: float) -> None:
        self.A = A
        self.o = o
        self.p = p
        self.b = b

    def __call__(self, t: float) -> float:
        return self.A*math.sin(self.o*t+self.p)+self.b


class Line:
    """
    判定线
    """

    def __init__(self, initial_position: float, initial_alpha: float, initial_note_speed: float) -> None:
        self.get_alpha = Linear_func(0, initial_alpha)
        self.get_position = Linear_func(0, initial_position)
        self.get_play_position = Linear_func(initial_note_speed, 0)


class Note:
    """
    音符
    """

    def __init__(self, start_time: float, end_time: float, judging_track: int, initial_showing_track: float, showing_position_offset: float, showing_length: float, line_id: int, properties: int) -> None:
        self.start_time = start_time
        self.end_time = end_time
        self.judging_track = judging_track
        self.get_showing_track = Linear_func(0, initial_showing_track)
        self.showing_position_offset = showing_position_offset
        self.showing_length = showing_length
        self.line_id = line_id
        for i, property in enumerate(NOTE_PROPERTIES):
            # 把 note 的“属性”当作类的属性直接用
            self.__dict__[property] = bool(properties & 1 << i)
