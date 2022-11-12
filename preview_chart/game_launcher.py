import json
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
    info = json.load(open(os.path.join(chart_dir, 'info.json'), encoding='utf-8'))
    chart_choices = {i['difficulty']+' '+i['number']+' By '+i['writer']: i for i in info['charts']}
    while True:
        if len(chart_choices) > 1:
            ch = easygui.choicebox('请选择谱面', info['title']+' - 预览谱面', chart_choices.keys())
            if ch is None:
                return
            chart_info = chart_choices[ch]
        else:  # 只有一个选项可用不了 choicebox 哦~
            chart_info = info['charts'][0]
        try:
            omgc_data, activated_notes, num_of_tracks = read_omgc(os.path.join(chart_dir, chart_info['difficulty']+'.omgc'), chart_info['md5'])
        except Exception:
            if len(chart_choices) > 1:
                continue
            else:
                return
        while True:
            input_data = easygui.multenterbox('请确认或更改播放参数', info['title']+' - 预览谱面', ['流速倍率(不小于1)', '音乐音量(0~1之间)'], [PREVIEW_DEFAULT_NOTE_SPEED_RATE, PREVIEW_DEFAULT_MUSIC_VOLUME])
            if input_data is None:
                return
            try:
                note_speed_rate, music_volume = map(float, input_data)
                assert note_speed_rate >= 1 and 0 <= music_volume <= 1
                break
            except Exception:
                easygui.msgbox('输入有误，请重新输入！', '好的')
        game_window = Window(info['title']+' '+chart_info['difficulty']+' '+chart_info['number'], os.path.join(chart_dir, info['illustration_file']), num_of_tracks)
        game = Game(omgc_data, activated_notes, os.path.join(chart_dir, info['music_file']), game_window, note_speed_rate, music_volume)
        game.main_loop()
        if len(chart_choices) == 1:
            return
