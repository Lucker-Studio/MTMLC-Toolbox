import os

import easygui

from .converter import malody2omegar
from .json_writer import write_json
from .mc_reader import read_mc


def main() -> None:
    chart_list = easygui.fileopenbox('选择 mc 文件（支持多选）', '导入 Malody 谱面', '*.mc', multiple=True)
    if not chart_list:
        return

    ok_list = []
    not_ok_list = []
    for chart in chart_list:
        try:
            chart_dir, file_name = os.path.split(chart)
            chart_name = os.path.splitext(file_name)[0]
            project_data = malody2omegar(*read_mc(chart))
            write_json(project_data, os.path.join(chart_dir, chart_name+'.json'))
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
    easygui.msgbox(msg, '导入 Malody 谱面', '好的')
