import hashlib
import json
import os
import shutil
import struct
import zipfile

import easygui

from .common import MTMLC_STRUCT_FORMAT


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
        os.makedirs(target_path, exist_ok=True)
    zipfile.ZipFile(zip_path).extractall(target_path)
    for dirpath, dirnames, filenames in os.walk(target_path):
        for name in dirnames+filenames:
            try:
                newname = name.encode('cp437').decode('utf-8')
                os.rename(os.path.join(target_path, dirpath, name), os.path.join(target_path, dirpath, newname))
            except UnicodeError:
                pass


def write_mtmlc(lines: list, notes: list, commands: list, mtmlc_path: str) -> None:
    """
    写入 mtmlc 谱面文件
    """

    with open(mtmlc_path, 'wb') as f:
        f.write('MTML'.encode('ascii'))
        data = [len(lines), len(notes), len(commands)]

        for line in lines:
            data.extend(line)

        for note in notes:
            data.extend(note)

        for time, cmd_type, parameters in commands:
            data.extend((time, cmd_type, len(parameters), *parameters))  # 将二维列表展开成一维并添加参数数量

        for i in data:
            f.write(struct.pack(MTMLC_STRUCT_FORMAT[type(i)], i))  # 将二进制数据写入文件


def pack_zip(files: dict, zip_path: str) -> None:
    """
    打包到 zip 文件
    """
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as f:
        for inside_path, outside_path in files.items():
            f.write(outside_path, inside_path)


def pack_folder(files: dict, folder_path: str) -> None:
    """
    打包到文件夹
    """
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)
    for inside_path, outside_path in files.items():
        shutil.copy(outside_path, os.path.join(folder_path, inside_path))


def save_file(title: str, file_type: str, default_name: str = '*') -> str:
    """
    保存文件对话框
    """
    if file_path := easygui.filesavebox(title, default=default_name+file_type):
        if not file_path.endswith(file_type):
            file_path += file_type
        return file_path


def get_md5(file_path: str) -> str:
    """
    获取文件 MD5 字符串
    """
    return hashlib.md5(open(file_path, 'rb').read()).hexdigest()
