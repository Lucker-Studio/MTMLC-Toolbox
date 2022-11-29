import easygui

from Core.common import SUPPORTED_ILLUSTRATION_FORMATS, SUPPORTED_MUSIC_FORMATS
from Core.project_exporter import export_project
from Core.file_io import pack_zip, save_file, write_json


def main() -> None:
    """
    手动导出
    """
    title = ''
    composer = ''
    illustrator = ''
    music_file = SUPPORTED_MUSIC_FORMATS[0]
    illustration_file = SUPPORTED_ILLUSTRATION_FORMATS[0]
    charts = []

    data = title, composer, illustrator
    while True:
        data = easygui.multenterbox('请输入歌曲信息：', '手动导出', ['曲名', '曲师', '画师'], data)
        if data is None:  # 关闭对话框
            return
        if not all(data):  # 存在空字符串
            easygui.msgbox('请将歌曲信息填写完整！', '手动导出', '哦~')
        else:
            title, composer, illustrator = data
            break

    music_file = easygui.fileopenbox('请选择歌曲音频', '手动导出', music_file, SUPPORTED_MUSIC_FORMATS)
    if music_file is None:
        return
    illustration_file = easygui.fileopenbox('请选择曲绘图片', '手动导出', illustration_file, SUPPORTED_ILLUSTRATION_FORMATS)
    if illustration_file is None:
        return

    while True:
        if len(charts) >= 1:  # 至少添加一张谱面
            # key 为谱面的显示名称，value 为谱面信息
            show_charts = {f'{i["difficulty"]} By {i["writer"]} ({i["path"]})': i for i in charts}
            ch = easygui.buttonbox(f'已添加 {len(charts)} 张谱面：\n'+'\n'.join(show_charts.keys()), '手动导出', ('继续添加', '完成添加', '删除谱面'))
            if ch is None:  # 关闭对话框
                return

            elif ch == '完成添加':
                song_info = {
                    'title': title,
                    'composer': composer,
                    'illustrator': illustrator,
                    'music_file': music_file,
                    'illustration_file': illustration_file,
                    'charts': charts
                }
                info_path = save_file('保存 mtmlinfo 文件', '.mtmlinfo', 'index')
                if info_path:
                    write_json(song_info, info_path)
                break

            elif ch == '删除谱面':
                if len(show_charts) == 1:
                    if easygui.ynbox(f'确认删除 {list(show_charts.keys())[0]}？', '手动导出', ('确认', '取消')):
                        charts = []
                else:
                    charts_to_delete = easygui.multchoicebox('请选择要删除的谱面（支持多选）', '手动导出', show_charts.keys())
                    for chart in charts_to_delete:
                        charts.remove(show_charts[chart])
                continue

        data = ('', '', '')
        while True:
            data = easygui.multenterbox(f'请输入第 {len(charts)+1} 张谱面信息：', '手动导出', ['难度', '谱师'], data)
            if data is None:  # 关闭对话框
                if len(charts) >= 1:
                    break  # 回到谱面列表
                else:
                    return
            if not all(data):  # 存在空字符串
                easygui.msgbox('请将谱面信息填写完整！', '手动导出', '哦~')
            else:
                difficulty, writer = data
                break

        if data is None:
            continue  # 回到谱面列表

        if mtmlproj_path := easygui.fileopenbox('请选择工程文件', '手动导出', '*.mtmlproj'):
            charts.append({'difficulty': difficulty,  'writer': writer, 'path': mtmlproj_path})

    files = export_project(**song_info)

    if mtmlz_path := save_file('保存 mtmlz 文件', '.mtmlz', title):
        pack_zip(files, mtmlz_path)
        easygui.msgbox('导出成功！', '手动导出', '好耶')
