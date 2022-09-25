import os

import easygui

from .read_malody import read_malody
from .write_omegar import write_omegar


def main() -> None:
    project_folder = easygui.diropenbox('选择文件夹', '导入 Malody 谱面')
    if not project_folder:
        return

    charts_path = []
    for i in os.listdir(project_folder):
        path = os.path.join(project_folder, i)
        if os.path.isfile(path):
            if path.endswith('.mc'):
                charts_path.append(path)

    if not charts_path:
        easygui.msgbox('未找到 Malody 谱面文件，请参照教程正确处理和选择文件夹！', '导入 Malody 谱面', '好的')
        return
    charts_data = {}
    for mc_path in charts_path:
        data = read_malody(mc_path)
        charts_data[data['project_name']] = data

    if len(charts_data) > 1:
        charts_name = easygui.multchoicebox('请选择要导入的谱面（可多选）', '导入 Malody 谱面', charts_data.keys())
        if charts_name is None:
            return
    else:
        charts_name = list(charts_data.keys())

    ok_list = []
    not_ok_list = []
    for name in charts_data.keys():
        if name in charts_name:
            try:
                write_omegar(charts_data[name], os.path.join(project_folder, name+'.json'))
                ok_list.append(name)
            except:
                not_ok_list.append(name)

    msg = f'{len(ok_list)} 个谱面导入成功'+'。；'[bool(ok_list)]
    for i in ok_list:
        msg += '\n'+i
    if not_ok_list:
        msg += f'\n{len(not_ok_list)} 个谱面导入失败：'
        for i in not_ok_list:
            msg += '\n'+i
    easygui.msgbox(msg, '导入 Malody 谱面', '好的')
