import struct

from .constants import *


def write_omgc(instructions: list, omgc_path: str) -> None:
    """
    将指令列表写入 omgc 谱面文件。
    """
    if DEBUG_MODE:
        debug_log = open('debug.log', 'w')
    instructions_expanded = [len(instructions)]  # 首个数据为指令总数
    for instruction in instructions:  # 注意此处指令已排序
        instructions_expanded.extend(instruction)  # 将二维列表展开成一维
        if DEBUG_MODE:
            print('\t'.join((str(instruction[0]), INSTR_NAME[instruction[1]], str(instruction[2:]))), file=debug_log)
    if DEBUG_MODE:
        debug_log.close()

    with open(omgc_path, 'wb') as f:
        for data in instructions_expanded:
            f.write(struct.pack({int: '>i', float: '>f'}[type(data)], data))
