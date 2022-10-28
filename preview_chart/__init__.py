import os
import tempfile
import zipfile

import easygui
from .omgc_reader import read_omgc


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
            ch = easygui.choicebox('请选择谱面', title+' 谱面预览', chart_choices.keys())
            if ch is None:
                break
            chart_info = chart_choices[ch]
        else:
            chart_info = charts_info[0]
        omgc_data = read_omgc(os.path.join(zip_dir, 'charts', chart_info[0]+'.omgc'), chart_info[3])
        if omgc_data is None:
            if len(chart_choices) > 1:
                continue
            else:
                break
