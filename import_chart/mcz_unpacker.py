import json
import os
import zipfile

from constants import *

from .converter import malody2omegar


def unpack_mcz(mcz_path: str, dir_path: str) -> list:
    """
    将 mcz 文件导入为文件夹
    """
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    zipfile.ZipFile(mcz_path).extractall(dir_path)
    info = {'illustrator': 'unknown', 'charts': []}
    for file_name in os.listdir(dir_path):
        chart_name, chart_ext = os.path.splitext(file_name)
        if chart_ext == '.mc':
            try:
                target = os.path.join(dir_path, chart_name+'.json')
                mc_data = json.load(open(os.path.join(dir_path, file_name), encoding='utf-8'))
                project_data = malody2omegar(mc_data)
                json.dump(project_data, open(target, 'w', encoding='utf-8'))
                info['charts'].append({
                    'difficulty': mc_data['meta']['version'],
                    'number': '0',
                    'writer': mc_data['meta'].get('creator', 'unknown'),
                    'json_path': target
                })
                info['title'] = mc_data['meta']['song']['title']
                info['composer'] = mc_data['meta']['song']['artist']
                info['music_path'] = os.path.join(dir_path, project_data['music_path'])
                if mc_data['meta'].get('backgronund'):
                    info['illustration_path'] = os.path.join(dir_path, mc_data['meta']['background'])
            except Exception:
                pass
    if 'illustration_path' not in info:
        info['illustration_path'] = os.path.join(RESOURCES_DIR, 'Malody.jpg')
    if len(info['charts']) == 0:
        raise Exception('不含有效谱面')
    return info
