import os
import zipfile


def unpack_mcz(mcz_path: str, dir_path: str) -> None:
    """
    将 mcz 文件导入为文件夹
    """
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    zipfile.ZipFile(mcz_path).extractall(dir_path)
