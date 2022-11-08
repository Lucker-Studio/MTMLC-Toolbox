import hashlib
import tempfile

from .converter import json2omgc
from .json_reader import read_json
from .omgc_writer import write_omgc


def batch_charts(title: str, composer: str, illustrator: str, charts_info: list) -> tuple:
    """
    批量处理谱面
    """

    for chart_info in charts_info:
        chart_info['omgc_path'] = tempfile.mkstemp()[1]  # 获取临时 omgc 文件名
        lines, notes, commands = json2omgc(*read_json(chart_info['json_path']))
        write_omgc(lines, notes, commands, chart_info['omgc_path'])
        chart_info['md5'] = hashlib.md5(open(chart_info['omgc_path'], 'rb').read()).hexdigest()  # 计算 omgc 文件 MD5

    info_path = tempfile.mkstemp()[1]  # 获取临时 info.txt 文件名
    with open(info_path, 'w', encoding='utf-8') as f:
        print(title, composer, illustrator, len(charts_info), sep='\n', file=f)  # 写入歌曲信息
        for chart_info in charts_info:
            print(chart_info['difficulty'], chart_info['diff_number'], chart_info['writer'], chart_info['md5'], sep='\n', file=f)  # 写入谱面信息

    return charts_info, info_path
