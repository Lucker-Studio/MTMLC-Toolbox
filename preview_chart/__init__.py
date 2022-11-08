import os
import tempfile
import zipfile

import easygui

from .game_controller import Game
from .omgc_reader import read_omgc
from .window_controller import Window


def main() -> None:
    zip_path = easygui.fileopenbox('打开 zip 谱面', '谱面预览', '*.zip')
    if zip_path is None:
        return
    zip_dir = tempfile.mkdtemp()
    zipfile.ZipFile(zip_path).extractall(zip_dir)
    title, composer, illustrator, n, *charts_info = open(os.path.join(zip_dir, 'info.txt'), encoding='utf-8').read().splitlines()
    charts_info = [[charts_info[i*4+j] for j in range(4)] for i in range(int(n))]
    chart_choices = {i[0]+' '+i[1]+' By '+i[2]: i for i in charts_info}
    while True:
        if len(chart_choices) > 1:
            ch = easygui.choicebox('请选择谱面', f'{title} - 谱面预览', chart_choices.keys())
            if ch is None:
                break
            chart_info = chart_choices[ch]
        else:  # 只有一个选项可用不了 choicebox 哦~
            chart_info = charts_info[0]
        difficulty, diff_number, chart_writer, omgc_md5 = chart_info
        omgc_data = read_omgc(os.path.join(zip_dir, 'charts', difficulty+'.omgc'), omgc_md5)
        if omgc_data is None:
            if len(chart_choices) > 1:
                continue
            else:  # 这里要是不 break 就死循环了
                break
        game_window = Window(f'{title} {difficulty} {diff_number}', os.path.join(zip_dir, 'illustration.png'))
        game = Game(omgc_data, os.path.join(zip_dir, 'music.mp3'), game_window)
        game.main_loop()
        if len(chart_choices) == 1:
            break
