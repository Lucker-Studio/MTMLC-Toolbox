import os

import easygui

from constants import *

from .game_controller import Game
from .omgc_reader import read_omgc
from .window_controller import Window


def launch(chart_dir: str) -> None:
    """
    游戏启动器
    """
    title, composer, illustrator, n, *charts_info = open(os.path.join(chart_dir, 'info.txt'), encoding='utf-8').read().splitlines()
    charts_info = [[charts_info[i*4+j] for j in range(4)] for i in range(int(n))]
    chart_choices = {i[0]+' '+i[1]+' By '+i[2]: i for i in charts_info}
    while True:
        if len(chart_choices) > 1:
            ch = easygui.choicebox('请选择谱面', f'{title} - 谱面预览', chart_choices.keys())
            if ch is None:
                return
            chart_info = chart_choices[ch]
        else:  # 只有一个选项可用不了 choicebox 哦~
            chart_info = charts_info[0]
        difficulty, number, chart_writer, omgc_md5 = chart_info
        omgc_data = read_omgc(os.path.join(chart_dir, 'charts', difficulty+'.omgc'), omgc_md5)
        if omgc_data is None:
            if len(chart_choices) > 1:
                continue
            else:
                return
        while True:
            input_data = easygui.multenterbox('请确认或更改播放参数', f'{title} - 谱面预览', ['流速倍率(不小于1)', '音乐音量(0~1之间)', '谱面偏移(单位:s)'], [PREVIEW_DEFAULT_NOTE_SPEED_RATE, PREVIEW_DEFAULT_MUSIC_VOLUME, PREVIEW_DEFAULT_CHART_OFFSET])
            if input_data is None:
                return
            try:
                note_speed_rate, music_volume, chart_offset = map(float, input_data)
                assert (note_speed_rate >= 1 and 0 <= music_volume <= 1)
                break
            except Exception:
                easygui.msgbox('输入有误，请重新输入！', '好的')
        game_window = Window(f'{title} {difficulty} {number}', os.path.join(chart_dir, 'illustration.png'))
        game = Game(omgc_data, os.path.join(chart_dir, 'music.mp3'), game_window, note_speed_rate, music_volume, chart_offset)
        game.main_loop()
        if len(chart_choices) == 1:
            return
