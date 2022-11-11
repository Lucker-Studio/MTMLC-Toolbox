import os
import shutil
import zipfile


def pack_to_zip(files: dict, zip_path: str) -> None:
    """
    打包到 zip 文件
    """

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as f:
        for inside_path, outside_path in files.items():
            f.write(outside_path, inside_path)


def pack_to_dir(files: dict, dir_path: str) -> None:
    """
    打包到文件夹
    """

    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    for inside_path, outside_path in files.items():
        shutil.copy(outside_path, os.path.join(dir_path, inside_path))
