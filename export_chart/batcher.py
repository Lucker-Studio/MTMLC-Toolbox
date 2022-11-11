import hashlib
import json
import os
import tempfile

from .converter import json2omgc
from .json_reader import read_json
from .omgc_writer import write_omgc


def batch_charts(title: str, composer: str, illustrator: str, music_path: str, illustration_path: str, charts_info: list) -> dict:
    """
    批量处理谱面
    """

    files = {}
    for chart_info in charts_info:
        omgc_path = tempfile.mkstemp()[1]  # 获取临时 omgc 文件名
        music_offset, bpm_list, line_list = read_json(chart_info.pop('json_path'))
        lines, notes, commands = json2omgc(music_offset, bpm_list, line_list)
        write_omgc(lines, notes, commands, omgc_path)
        files[chart_info['difficulty']+'.omgc'] = omgc_path
        chart_info['md5'] = hashlib.md5(open(omgc_path, 'rb').read()).hexdigest()  # 计算 omgc 文件 MD5

    info = {'title': title, 'composer': composer, 'illustrator': illustrator}
    info['music_file'] = 'music'+os.path.splitext(music_path)[1]
    info['illustration_file'] = 'illustration'+os.path.splitext(illustration_path)[1]
    info['charts'] = charts_info
    files['info.json'] = tempfile.mkstemp()[1]  # 获取临时 info.json 文件名
    files[info['music_file']] = music_path
    files[info['illustration_file']] = illustration_path
    json.dump(info, open(files['info.json'], 'w', encoding='utf-8'))

    return files
