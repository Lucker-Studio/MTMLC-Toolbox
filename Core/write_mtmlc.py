import struct

from .common import MTMLC_STRUCT_FORMAT


def write_mtmlc(lines: list, notes: list, commands: list, mtmlc_path: str) -> None:
    """
    将指令列表写入 mtmlc 谱面文件
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
