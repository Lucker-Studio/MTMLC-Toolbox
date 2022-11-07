import struct

from constants import *


def write_omgc(lines: list, notes: list, commands: list, omgc_path: str) -> None:
    """
    将指令列表写入 omgc 谱面文件。
    """

    if TOOLBOX_DEBUG_MODE:
        debug_log = open('debug.log', 'w', encoding='utf-8')

    def print_log(*data):
        if TOOLBOX_DEBUG_MODE:
            print(*map(lambda x: round(x, 3) if type(x) == float else x, data), sep='\t', file=debug_log)

    print_log('LINE:')
    lines_expanded = []
    for line in lines:
        lines_expanded.extend(line)
        print_log(*line)

    print_log('NOTE:')
    notes_expanded = []
    for note in notes:
        notes_expanded.extend(note)
        print_log(*note)

    print_log('CMD:')
    commands_expanded = []
    for time, cmd_type, parameters in commands:
        commands_expanded.extend((time, cmd_type, len(parameters), *parameters))  # 将二维列表展开成一维并添加参数数量
        print_log(time, CMD_NAME[cmd_type]+f'({cmd_type})', len(parameters), parameters)

    print_log('META:')
    meta = [OMGC_WRITING_VERSION]
    meta.extend(map(len, (lines_expanded, lines, notes_expanded, notes, commands_expanded, commands)))
    print_log(*meta)

    with open(omgc_path, 'wb') as f:
        f.write('omgc'.encode('ascii'))
        for data in meta+lines_expanded+notes_expanded+commands_expanded:
            # 将二进制数据写入文件
            f.write(struct.pack(OMGC_STRUCT_FORMAT[type(data)], data))

    if TOOLBOX_DEBUG_MODE:
        debug_log.close()
