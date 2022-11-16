import os
import tempfile

from common import *

from .converter import omg2omgc
from .omgc_writer import write_omgc


def batch_charts(title: str, composer: str, illustrator: str, music_file: str, illustration_file: str, charts: list, dir_path: str = '') -> dict:
    """
    批量处理谱面
    """

    files = {}
    for chart_info in charts:
        omgc_path = tempfile.mkstemp()[1]  # 获取临时 omgc 文件名
        project_data = read_json(os.path.join(dir_path, chart_info.pop('omg_path')))
        lines, notes, commands = omg2omgc(project_data)
        write_omgc(lines, notes, commands, omgc_path)
        files[chart_info['difficulty']+'.omgc'] = omgc_path
        chart_info['md5'] = get_md5(omgc_path)  # 计算 omgc 文件 MD5

    song_info = {'title': title, 'composer': composer, 'illustrator': illustrator}
    song_info['music_file'] = 'music'+os.path.splitext(music_file)[1]
    song_info['illustration_file'] = 'illustration'+os.path.splitext(illustration_file)[1]
    song_info['charts'] = charts
    files['index.omginfo'] = tempfile.mkstemp()[1]
    files[song_info['music_file']] = os.path.join(dir_path, music_file)
    files[song_info['illustration_file']] = os.path.join(dir_path, illustration_file)
    write_json(song_info, files['index.omginfo'])

    return files
