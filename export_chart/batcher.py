import os
import tempfile

from common import *

from .converter import proj2chart
from .chart_writer import write_mtmlc


def batch_project(title: str, composer: str, illustrator: str, music_file: str, illustration_file: str, charts: list, dir_path: str = '') -> dict:
    """
    批量处理工程文件
    """

    files = {}
    for chart_info in charts:
        mtmlc_path = tempfile.mkstemp()[1]  # 获取临时 mtmlc 文件名
        project_data = read_json(os.path.join(dir_path, chart_info.pop('mtmlproj_path')))
        lines, notes, commands = proj2chart(project_data)
        write_mtmlc(lines, notes, commands, mtmlc_path)
        files[chart_info['difficulty']+'.mtmlc'] = mtmlc_path
        chart_info['md5'] = get_md5(mtmlc_path)  # 计算 mtmlc 文件 MD5

    song_info = {'title': title, 'composer': composer, 'illustrator': illustrator}
    song_info['music_file'] = 'music'+os.path.splitext(music_file)[1]
    song_info['illustration_file'] = 'illustration'+os.path.splitext(illustration_file)[1]
    song_info['charts'] = charts
    files['index.mtmlinfo'] = tempfile.mkstemp()[1]
    files[song_info['music_file']] = os.path.join(dir_path, music_file)
    files[song_info['illustration_file']] = os.path.join(dir_path, illustration_file)
    write_json(song_info, files['index.mtmlinfo'])

    return files
