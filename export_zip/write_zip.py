import hashlib
import tempfile
import zipfile

from .read_json import read_json
from .write_omgc import write_omgc


def write_zip(music_path: str, illustration_path: str,
               title: str, composer: str, illustrator: str,
               charts_info: list, zip_path: str) -> None:
    """
    打包成 zip 文件。
    """
    for chart_info in charts_info:
        chart_info['omgc_path'] = tempfile.mkstemp()[1]  # 获取临时 omgc 文件名
        lines,notes,commands = read_json(chart_info['json_path'])
        write_omgc(lines,notes,commands, chart_info['omgc_path'])
        chart_info['md5'] = hashlib.md5(open(chart_info['omgc_path'], 'rb').read()).hexdigest()  # 计算 omgc 文件 MD5

    info_path = tempfile.mkstemp()[1]  # 获取临时 info.txt 文件名
    with open(info_path, 'w', encoding='utf-8') as f:
        print(title, composer, illustrator, len(charts_info), sep='\n', file=f)  # 写入歌曲信息
        for chart_info in charts_info:
            print(chart_info['difficulty'], chart_info['diff_number'], chart_info['writer'], chart_info['md5'], sep='\n', file=f)  # 写入谱面信息

    with zipfile.ZipFile(zip_path, 'w') as f:
        f.write(info_path, 'info.txt', zipfile.ZIP_DEFLATED)
        f.write(music_path, 'music.mp3', zipfile.ZIP_DEFLATED)
        f.write(illustration_path, 'illustration.png', zipfile.ZIP_DEFLATED)
        for chart_info in charts_info:
            f.write(chart_info['omgc_path'], 'charts/' + chart_info['difficulty']+'.omgc', zipfile.ZIP_DEFLATED)
