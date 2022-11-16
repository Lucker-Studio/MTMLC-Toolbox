import hashlib
import struct

from common import *

from .base import *


def read_omgc(omgc_path: str, omgc_md5: str) -> tuple:
    """
    读取 omgc 谱面文件
    """

    chart_data = open(omgc_path, 'rb').read()
    if hashlib.md5(chart_data).hexdigest() != omgc_md5:
        raise Exception('谱面文件 MD5 不匹配，可能已被篡改')

    def read_4byte():
        """
        从 omgc 文件读取 4 字节（一个数据）
        """
        index = 0
        while True:
            yield chart_data[index:index+4]
            index += 4
    read_4byte = read_4byte()

    # 文件开头 4 字节必须是“omgc”的 ASCII 码
    if next(read_4byte).decode('ascii') != 'omgc':
        raise Exception('谱面文件头不符合 omgc 格式')

    def read_data(data_type):
        """
        读取一个指定类型的数据
        """
        return struct.unpack(OMGC_STRUCT_FORMAT[data_type], next(read_4byte))[0]

    def read_multi_data(*args):
        """
        读取多个指定类型的数据
        """
        return list(map(read_data, args))

    omgc_version = read_data(int)
    if omgc_version not in PREVIEW_SUPPORTED_OMGC_VERSIONS:
        raise Exception(f'暂不支持此版本（{omgc_version}）的 omgc 文件')

    line_count, note_count, cmd_count = read_multi_data(int, int, int)

    lines = []
    for i in range(line_count):
        lines.append(Line(*read_multi_data(float, float, float)))

    notes = []
    num_of_tracks = 0
    activated_notes_map = {}
    for i in range(note_count):
        note_data = read_multi_data(float, float, int, float, float, float, int, int, int)
        num_of_tracks = max(num_of_tracks, note_data[2]+1)
        if note_data.pop():
            activated_notes_map.setdefault(note_data[2], [])
            activated_notes_map[note_data[2]].append(i)
        notes.append(Note(*note_data))

    commands = []
    for i in range(cmd_count):
        cmd_time, cmd_type, cmd_param_count = read_multi_data(float, int, int)
        if cmd_type in COMMAND_PARAM_TYPE:
            cmd_params = read_multi_data(*COMMAND_PARAM_TYPE[cmd_type])
            commands.append((cmd_time, cmd_type, cmd_params))
        else:
            # 跳过未知类型的指令
            for j in range(cmd_param_count):
                next(read_4byte)

    activated_notes = []
    for i in range(num_of_tracks):
        activated_notes.append(activated_notes_map.get(i, []))

    return (lines, notes, commands), activated_notes, num_of_tracks
