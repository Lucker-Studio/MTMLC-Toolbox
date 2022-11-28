import os

import easygui
import pygame

from ..file_io import read_json
from .chart_reader import read_mtmlc
from .config import DEFAULT_MUSIC_VOLUME, DEFAULT_SPEED_RATE
from .game_controller import Game
from .window_controller import Window


def preview_chart(chart_dir: str) -> None:
    """
    预览已解压的谱面文件夹
    """
    song_info = read_json(os.path.join(chart_dir, 'index.mtmlinfo'))
    chart_choices = {i['difficulty']+' By '+i['writer']: i for i in song_info['charts']}
    while True:
        if len(chart_choices) > 1:
            ch = easygui.choicebox('请选择谱面', song_info['title']+' - 预览谱面', chart_choices.keys())
            if ch is None:
                return
            chart_info = chart_choices[ch]
        else:  # 只有一个选项可用不了 choicebox 哦~
            chart_info = song_info['charts'][0]
        try:
            mtmlc_data, activated_notes, num_of_tracks = read_mtmlc(os.path.join(chart_dir, chart_info['difficulty']+'.mtmlc'), chart_info['md5'])
        except Exception:
            easygui.exceptionbox('无法读取谱面文件')
            if len(chart_choices) > 1:
                continue
            else:
                return
        while True:
            input_data = easygui.multenterbox('请确认或更改播放参数', song_info['title']+' - 预览谱面', ['流速倍率(不小于1)', '音乐音量(0~1之间)'], [DEFAULT_SPEED_RATE, DEFAULT_MUSIC_VOLUME])
            if input_data is None:
                return
            try:
                speed_rate, music_volume = map(float, input_data)
                assert speed_rate >= 1 and 0 <= music_volume <= 1
                break
            except Exception:
                easygui.msgbox('输入有误，请重新输入！', '好的')
        try:
            game_window = Window(song_info['title']+' '+chart_info['difficulty'], os.path.join(chart_dir, song_info['illustration_file']), num_of_tracks)
            game = Game(mtmlc_data, activated_notes, os.path.join(chart_dir, song_info['music_file']), game_window, speed_rate, music_volume)
            game.main_loop()
        except Exception as e:
            pygame.quit()
            raise e
        if len(chart_choices) == 1:
            return
