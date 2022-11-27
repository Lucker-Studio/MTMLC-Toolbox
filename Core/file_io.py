import hashlib
import json
import os
import shutil
import zipfile


def read_json(json_path: str) -> dict:
    """
    读取 json 文件
    """
    return json.load(open(json_path, encoding='utf-8'))


def write_json(data: dict, json_path: str) -> None:
    """
    写入 json 文件
    """
    json.dump(data, open(json_path, 'w', encoding='utf-8'))


def unpack_zip(zip_path: str, target_path: str) -> None:
    """
    解包 zip 文件
    """
    if not os.path.isdir(target_path):
        os.makedirs(target_path)
    zipfile.ZipFile(zip_path).extractall(target_path)
    for dirpath, dirnames, filenames in os.walk(target_path):
        for name in dirnames+filenames:
            try:
                newname = name.encode('cp437').decode('utf-8')
                os.rename(os.path.join(target_path, dirpath, name), os.path.join(target_path, dirpath, newname))
            except UnicodeError:
                pass


def pack_zip(files: dict, zip_path: str) -> None:
    """
    打包到 zip 文件
    """

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as f:
        for inside_path, outside_path in files.items():
            f.write(outside_path, inside_path)


def pack_dir(files: dict, dir_path: str) -> None:
    """
    打包到文件夹
    """

    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    for inside_path, outside_path in files.items():
        shutil.copy(outside_path, os.path.join(dir_path, inside_path))


def get_md5(file_path: str) -> str:
    """
    获取文件 MD5 字符串
    """

    return hashlib.md5(open(file_path, 'rb').read()).hexdigest()
