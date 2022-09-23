import json


def read_malody(mc_path: str) -> dict:
    """
    将 Malody 谱面读取为含 project_name、beats、notes 的 dict。
    """
    mc_data = json.load(open(mc_path))
    bpm_list = sorted((i['beat'][0]+i['beat'][1]/i['beat'][2], i['bpm']) for i in mc_data['time'])

    project_data = {'project_name': mc_data['meta']['song']['title']+' '+mc_data['meta']['version'], 'beats': beats, 'notes': notes}
