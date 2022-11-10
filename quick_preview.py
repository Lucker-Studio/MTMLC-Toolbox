import json
import tempfile

import easygui

from export_chart.batcher import batch_charts
from export_chart.packer import pack_to_dir
from preview_chart.game_launcher import launch


def main() -> None:
    template_path = easygui.fileopenbox('请选择模板文件', '快速预览', '*.tpl')
    if template_path is None:  # 未选择文件
        return
    # 读取 json 数据
    template_data = tuple(json.load(open(template_path, encoding='utf-8')))  # 为了比较数据是否改变，需要转为不可变类型
    music_path, illustration_path, title, composer, illustrator, charts_info = template_data
    charts_info, info_path = batch_charts(title, composer, illustrator, charts_info)
    chart_dir = tempfile.mkdtemp()
    pack_to_dir(music_path, illustration_path, charts_info, info_path, chart_dir)
    launch(chart_dir)
