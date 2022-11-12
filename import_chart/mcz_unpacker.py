import json
import os
import zipfile

from constants import *

from .converter import malody2omegar
from .mc_reader import read_mc


def unpack_mcz(mcz_path: str, dir_path: str) -> list:
    """
    将 mcz 文件导入为文件夹
    """
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    zipfile.ZipFile(mcz_path).extractall(dir_path)
    info = {'illustration_path': os.path.join(RESOURCES_DIR, 'Default.jpg'), 'charts': []}
    for file_name in os.listdir(dir_path):
        chart_name, chart_ext = os.path.splitext(file_name)
        if chart_ext == '.mc':
            try:
                target = os.path.join(dir_path, chart_name+'.json')
                mc_data, chart_info, song_info = read_mc(os.path.join(dir_path, file_name))
                project_data = malody2omegar(mc_data)
                json.dump(project_data, open(target, 'w', encoding='utf-8'))
                info['music_path'] = os.path.join(dir_path, project_data['music_file'])
                if project_data['illustration_file']:
                    info['illustration_path'] = os.path.join(dir_path, project_data['illustration_file'])
                info['charts'].append({**chart_info, 'json_path': target})
                for key, value in song_info.items():
                    if value:
                        info[key] = value
            except Exception:
                pass
    if 'title' not in info:
        info['title'] = 'Song'
    if 'composer' not in info:
        info['composer'] = 'Unknown'
    if 'illustrator' not in info:
        info['illustrator'] = 'Unknown'
    if len(info['charts']) == 0:
        raise Exception('不含有效谱面')
    else:
        json.dump(info, open(os.path.join(dir_path, 'info.json'), 'w', encoding='utf-8'))
        return info
