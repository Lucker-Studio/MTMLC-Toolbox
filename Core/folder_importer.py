import os
import traceback

from .common import RESOURCES_PATH
from .file_io import read_json, write_json
from .malody_importer import mc2mtmlproj


def import_folder(folder_path: str) -> list:
    """
    导入文件夹
    返回：song_info
    """
    song_info = {'charts': []}
    for file_name in os.listdir(folder_path):
        chart_name, chart_ext = os.path.splitext(file_name)
        if chart_ext == '.mc':
            try:
                target = os.path.join(folder_path, chart_name+'.mtmlproj')
                mc_data = read_json(os.path.join(folder_path, file_name))
                song_info_upd, chart_info, project_data = mc2mtmlproj(mc_data)
                song_info.update(song_info_upd)
                write_json(project_data, target)
                song_info['charts'].append({**chart_info, 'path': target})
            except Exception:
                traceback.print_exc()
    if len(song_info['charts']) == 0:
        raise Exception('不含有效谱面')
    else:
        song_info.setdefault('title', 'Untitled Song')
        song_info.setdefault('composer', 'Unknown')
        song_info.setdefault('illustrator', 'Unknown')
        song_info.setdefault('illustration_file', os.path.join(RESOURCES_PATH, 'Default.jpg'))
        write_json(song_info, os.path.join(folder_path, 'index.mtmlinfo'))
        return song_info
