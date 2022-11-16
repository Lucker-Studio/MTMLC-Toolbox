import json
import os

from constants import *

from .converter import malody2omegar


def import_dir(dir_path: str) -> list:
    """
    导入文件夹
    """
    song_info = {'charts': []}
    for file_name in os.listdir(dir_path):
        chart_name, chart_ext = os.path.splitext(file_name)
        if chart_ext == '.mc':
            try:
                target = os.path.join(dir_path, chart_name+'.omg')
                mc_data = json.load(open(os.path.join(dir_path, file_name), encoding='utf-8'))
                song_info, chart_info, project_data = malody2omegar(mc_data)
                json.dump(project_data, open(target, 'w', encoding='utf-8'))
                song_info['charts'].append({**chart_info, 'omg_path': target})
                for key, value in chart_info.items():
                    if value:
                        song_info[key] = value
            except Exception:
                pass
    if len(song_info['charts']) == 0:
        raise Exception('不含有效谱面')
    else:
        song_info.setdefault('title', 'Untitled Song')
        song_info.setdefault('composer', 'Unknown')
        song_info.setdefault('illustration_file', os.path.join(RESOURCES_DIR, 'Default.jpg'))
        json.dump(song_info, open(os.path.join(dir_path, 'index.omginfo'), 'w', encoding='utf-8'))
        return song_info
