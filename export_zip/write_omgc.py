import struct

from constants import *


def write_omgc(commands: list, omgc_path: str) -> None:
    """
    将指令列表写入 omgc 谱面文件。
    """
    if DEBUG_MODE:
        debug_log = open('debug.log', 'w', encoding='utf-8')
    commands_expanded = [len(commands)]  # 指令个数
    for time, cmd_type, parameters in commands:  # 此处指令已排序
        commands_expanded.extend((time, cmd_type, len(parameters), *parameters))  # 将二维列表展开成一维并添加参数数量
        if DEBUG_MODE:
            print('\t'.join((str(time), CMD_NAME[cmd_type], str(parameters))), file=debug_log)  # 输出可读指令到调试日志
    commands_expanded.insert(0, len(commands_expanded))  # 数据个数
    if DEBUG_MODE:
        debug_log.close()

    with open(omgc_path, 'wb') as f:
        for data in commands_expanded:
            # 将二进制数据写入文件
            f.write(struct.pack({int: '<I', float: '<f'}[type(data)], data))
