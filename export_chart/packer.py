import os
import shutil
import zipfile


def pack_to_zip(info_path: str, music_path: str, illustration_path: str,  charts_info: list, zip_path: str) -> None:
    """
    打包到 zip 文件
    """

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as f:
        f.write(info_path, 'info.txt')
        f.write(music_path, 'music.mp3')
        f.write(illustration_path, 'illustration.png')
        for chart_info in charts_info:
            f.write(chart_info['omgc_path'], 'charts/' + chart_info['difficulty']+'.omgc')


def pack_to_dir(music_path: str, illustration_path: str,  charts_info: list, info_path: str, dir_path: str) -> None:
    """
    打包到文件夹
    """

    if not os.path.isdir(os.path.join(dir_path, 'charts')):
        os.makedirs(os.path.join(dir_path, 'charts'))  # 创建两层文件夹，一步到位
    shutil.copy(info_path, os.path.join(dir_path, 'info.txt'))
    shutil.copy(music_path, os.path.join(dir_path, 'music.mp3'))
    shutil.copy(illustration_path, os.path.join(dir_path, 'illustration.png'))
    for chart_info in charts_info:
        shutil.copy(chart_info['omgc_path'], os.path.join(dir_path, 'charts', chart_info['difficulty']+'.omgc'))
