import json


def read_mc(mc_path: str) -> tuple:
    """
    读取 mc 谱面。
    """
    mc_data = json.load(open(mc_path, encoding='utf-8'))
    return mc_data['meta'], mc_data['time'], mc_data.get('effect', []), mc_data['note']
