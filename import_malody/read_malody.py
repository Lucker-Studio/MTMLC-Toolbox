import json


def read_malody(mc_path: str) -> dict:
    """
    将 Malody 谱面读取为含 project_name、beats、notes 的 dict。
    """
