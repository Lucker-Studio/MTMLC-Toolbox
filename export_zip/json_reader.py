import json

from constants import *


def read_json(json_path: str) -> tuple:
    """
    将 json 项目文件读取为指令列表。
    """

    json_data = json.load(open(json_path, encoding='utf-8'))  # 读取 json 数据
    return json_data['music_offset'], json_data['bpm_list'], json_data['global_speed_key_points'], json_data['line_list']
