import easygui

from common import *

from .batcher import batch_charts


def main() -> None:
    mode = easygui.ynbox('请选择导出模式', '导出谱面', ('使用 omginfo 自动导出', '手动设置信息'))
    if mode is None:
        return
    elif mode:
        info_path = easygui.fileopenbox('打开 omginfo 文件', '导出谱面', '*.omginfo')
        if info_path is None:
            return
        song_info = read_json(info_path)
    else:
        # 不使用 omginfo 时的默认信息
        title = ''
        composer = ''
        illustrator = ''
        music_file = OMGZ_SUPPORTED_MUSIC_FORMATS[0]
        illustration_file = OMGZ_SUPPORTED_ILLUSTRATION_FORMATS[0]
        charts = []

        data = (title, composer, illustrator)  # 默认信息，可能来自于模板
        while True:
            data = easygui.multenterbox('请输入歌曲信息：', '导出谱面', ['曲名', '曲师', '画师'], data)
            if data is None:  # 关闭对话框
                return
            if not all(data):  # 存在空字符串
                easygui.msgbox('请将歌曲信息填写完整！', '导出谱面', '哦~')
            else:
                title, composer, illustrator = data
                break

        music_file = easygui.fileopenbox('请选择歌曲音频', '导出谱面', music_file, OMGZ_SUPPORTED_MUSIC_FORMATS)
        if music_file is None:
            return
        illustration_file = easygui.fileopenbox('请选择曲绘图片', '导出谱面', illustration_file, OMGZ_SUPPORTED_ILLUSTRATION_FORMATS)
        if illustration_file is None:
            return

        while True:
            if len(charts) >= 1:  # 至少添加一张谱面
                # key 为谱面的显示名称，value 为谱面信息
                show_charts = {f'{i["difficulty"]} By {i["writer"]} ({i["omg_path"]})': i for i in charts}
                ch = easygui.buttonbox(f'已添加 {len(charts)} 张谱面：\n'+'\n'.join(show_charts.keys()), '导出谱面', ('继续添加', '完成添加', '删除谱面'))
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
                    info_path = easygui.filesavebox('保存 omginfo 文件', '导出谱面', 'index.omginfo')
                    if info_path:
                        write_json(song_info, info_path)
                    break

                elif ch == '删除谱面':
                    if len(show_charts) == 1:
                        if easygui.ynbox(f'确认删除 {list(show_charts.keys())[0]}？', '导出谱面', ('确认', '取消')):
                            charts = []
                    else:
                        charts_to_delete = easygui.multchoicebox('请选择要删除的谱面（支持多选）', '导出谱面', show_charts.keys())
                        for chart in charts_to_delete:
                            charts.remove(show_charts[chart])
                    continue

            data = ('', '', '')
            while True:
                data = easygui.multenterbox(f'请输入第 {len(charts)+1} 张谱面信息：', '导出谱面', ['难度', '谱师'], data)
                if data is None:  # 关闭对话框
                    if len(charts) >= 1:
                        break  # 回到谱面列表
                    else:
                        return
                if not all(data):  # 存在空字符串
                    easygui.msgbox('请将谱面信息填写完整！', '导出谱面', '哦~')
                else:
                    difficulty, writer = data
                    break

            if data is None:
                continue  # 回到谱面列表

            omg_path = easygui.fileopenbox('请选择谱面工程文件', '导出谱面', '*.omg')
            if omg_path is None:
                continue  # 回到谱面列表
            charts.append({'difficulty': difficulty,  'writer': writer, 'omg_path': omg_path})

    omgz_path = easygui.filesavebox('保存 omgz 文件', default=song_info['title']+'.omgz')
    if omgz_path is None:  # 未保存文件
        return
    files = batch_charts(**song_info)
    pack_zip(files, omgz_path)
    easygui.msgbox('导出成功！', '导出谱面', '好耶')
