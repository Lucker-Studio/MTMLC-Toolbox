import pickle

import easygui

from .write_omgz import write_omgz


def main() -> None:
    title = ''
    composer = ''
    illustrator = ''
    music_path = '*.ogg'
    illustration_path = '*.png'
    charts_info = []
    omgz_path = ''

    if easygui.ynbox('是否要使用已有的模板？', '导出 OMGZ 文件', ('是', '否')):
        pickle_path = easygui.fileopenbox('请选择生成设置文件', '导出 OMGZ 文件', '*.pkl')
        try:
            music_path, illustration_path, title, composer, illustrator,  charts_info = pickle.load(open(pickle_path, 'rb'))
        except:
            easygui.msgbox('未成功读取模板文件，将不使用模板。')

    data = title, composer, illustrator
    while True:
        data = easygui.multenterbox(
            '请输入歌曲信息：', '导出 OMGZ 文件', ['曲名', '曲师', '画师'], data)
        if not data:
            return
        if not all(data):
            easygui.msgbox('请将歌曲信息填写完整！', '导出 OMGZ 文件', '哦~')
        else:
            title, composer, illustrator = data
            break

    music_path = easygui.fileopenbox('请选择歌曲音频', '导出 OMGZ 文件', music_path)
    if not music_path:
        return
    illustration_path = easygui.fileopenbox('请选择曲绘图片', '导出 OMGZ 文件', illustration_path)
    if not illustration_path:
        return

    while True:
        if charts_info:  # 至少添加一张谱面
            show_charts = {f'{i["difficulty"]} {i["diff_number"]} By {i["writer"]} ({i["json_path"]})': i for i in charts_info}
            ch = easygui.buttonbox(f'已添加 {len(charts_info)} 张谱面：\n'+'\n'.join(show_charts.keys()), '导出 OMGZ 文件', ('继续添加', '完成添加', '删除谱面'))
            if not ch:
                return
            if ch == '完成添加':
                if not omgz_path:
                    omgz_path = title+'.omgz'
                omgz_path = easygui.filesavebox('保存 OMGZ 文件', default=omgz_path)
                if omgz_path:
                    try:
                        write_omgz(music_path, illustration_path, title, composer, illustrator, charts_info, omgz_path)
                        easygui.msgbox('导出成功！', '导出 OMGZ 文件', '好耶')
                        if easygui.ynbox('是否保存模板供以后使用？', '导出 OMGZ 文件', ('是', '否')):
                            pickle_path = easygui.filesavebox('保存生成设置', '导出 OMGZ 文件', title+'.pkl')
                            if pickle_path:
                                pickle.dump((music_path, illustration_path, title, composer, illustrator, charts_info, omgz_path), open(pickle_path, 'wb'))
                                easygui.msgbox('生成设置保存成功！', '导出 OMGZ 文件', '好耶')
                    except:
                        easygui.exceptionbox('出错啦！', '导出 OMGZ 文件')
                    return
            if ch == '删除谱面':
                charts_to_delete = easygui.multchoicebox('请选择要删除的谱面（支持多选）', '导出 OMGZ 文件', show_charts.keys())
                for chart in charts_to_delete:
                    charts_info.remove(show_charts[chart])
                continue

        data = ['']*3
        while True:
            data = easygui.multenterbox(f'请输入第 {len(charts_info)+1} 张谱面信息：', '导出 OMGZ 文件', ['难度', '定数', '谱师'], data)
            if not data:
                if charts_info:
                    break
                else:
                    return
            if not all(data):
                easygui.msgbox('请将谱面信息填写完整！', '导出 OMGZ 文件', '哦~')
            else:
                difficulty, diff_number, writer = data
                break

        if data:
            json_path = easygui.fileopenbox('请选择谱面工程文件', '导出 OMGZ 文件', '*.json')
            if json_path:
                charts_info.append({'difficulty': difficulty, 'diff_number': diff_number, 'writer': writer, 'json_path': json_path})
