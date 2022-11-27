import struct

from common import *


def write_mtmlc(lines: list, notes: list, commands: list, mtmlc_path: str) -> None:
    """
    将指令列表写入 mtmlc 谱面文件
    """

    meta = [len(lines), len(notes), len(commands)]

    lines_expanded = []
    for line in lines:
        lines_expanded.extend(line)

    notes_expanded = []
    for note in notes:
        notes_expanded.extend(note)

    commands_expanded = []
    for time, cmd_type, parameters in commands:
        commands_expanded.extend((time, cmd_type, len(parameters), *parameters))  # 将二维列表展开成一维并添加参数数量

    with open(mtmlc_path, 'wb') as f:
        f.write('MTML'.encode('ascii'))
        for data in meta+lines_expanded+notes_expanded+commands_expanded:
            # 将二进制数据写入文件
            f.write(struct.pack(MTMLC_STRUCT_FORMAT[type(data)], data))
