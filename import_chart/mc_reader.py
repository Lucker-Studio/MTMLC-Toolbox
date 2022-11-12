import json


def read_mc(mc_path: str) -> tuple:
    """
    读取 mc 文件数据
    """
    mc_data = json.load(open(mc_path, encoding='utf-8'))
    chart_info = {
        'difficulty': mc_data['meta'].get('version'),
        'number': '0',
        'writer': mc_data['meta'].get('creator')
    }
    if not chart_info['difficulty']:
        chart_info['difficulty'] = 'Default'
    if not chart_info['writer']:
        chart_info['writer'] = 'Unknown'
    song_info = {
        'title': mc_data['meta']['song'].get('title'),
        'composer': mc_data['meta']['song'].get('artist')
    }
    return mc_data, chart_info, song_info
