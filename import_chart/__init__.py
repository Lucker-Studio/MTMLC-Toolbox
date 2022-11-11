import json
import os

import easygui

from .converter import malody2omegar
from .mcz_unpacker import unpack_mcz


def main() -> None:
    chart_list = easygui.fileopenbox('选择文件（支持多选）', '导入谱面', '*.mcz', ['*.mcz', '*.mc'], multiple=True)
    if not chart_list:
        return

    ok_list = []
    not_ok_list = []
    for chart in chart_list:
        try:
            chart_dir, file_name = os.path.split(chart)
            chart_name, chart_ext = os.path.splitext(file_name)
            if chart_ext == '.mcz':
                target = os.path.join(chart_dir, chart_name)
                if os.path.isdir(target) and not easygui.ynbox(f'文件夹 {chart_name} 已存在，确认要覆盖其中的文件吗？', '导入谱面', ('确认', '取消')):
                    raise Exception('已存在同名文件夹')
                unpack_mcz(chart, target)
            elif chart_ext == '.mc':
                target = os.path.join(chart_dir, chart_name+'.json')
                if os.path.isfile(target) and not easygui.ynbox(f'文件 {chart_name} 已存在，确认要覆盖吗？', '导入谱面', ('确认', '取消')):
                    raise Exception('已存在同名文件')
                json.dump(malody2omegar(json.load(open(chart, encoding='utf-8'))), open(target, 'w', encoding='utf-8'))
            else:
                raise Exception('不支持的文件格式！')
            ok_list.append(file_name)
        except Exception as e:
            not_ok_list.append(f'{file_name}:{repr(e)}')

    msg = f'{len(ok_list)} 个谱面导入成功'+'。；'[bool(ok_list)]
    for i in ok_list:
        msg += '\n'+i
    if not_ok_list:
        msg += f'\n{len(not_ok_list)} 个谱面导入失败：'
        for i in not_ok_list:
            msg += '\n'+i
    easygui.msgbox(msg, '导入谱面', '好的')
