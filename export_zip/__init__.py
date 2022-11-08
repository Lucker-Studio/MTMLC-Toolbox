import json
import os

import easygui

from .zip_writer import write_zip


def main() -> None:
    # 不使用模板时的默认信息
    title = ''
    composer = ''
    illustrator = ''
    music_path = '*.mp3'
    illustration_path = '*.png'
    charts_info = []

    using_template = easygui.ynbox('是否要使用已有的模板？', '导出 ZIP 文件', ('是', '否'))
    if using_template is None:  # 关闭对话框
        return
    elif using_template:  # 选择“是”
        template_path = str(easygui.fileopenbox('请选择模板文件', '导出 ZIP 文件', '*.tpl'))
        if template_path is None:  # 未选择文件
            return
        try:
            # 读取 json 数据
            template_data = tuple(json.load(open(template_path, encoding='utf-8')))  # 为了比较数据是否改变，需要转为不可变类型
            music_path, illustration_path, title, composer, illustrator, charts_info = template_data
        except:
            easygui.msgbox('未成功读取模板文件，将不使用模板。', '导出 ZIP 文件', '好的')
            using_template = False
    else:  # 选择“否”
        using_template = False

    skip = False
    if using_template:
        if os.path.isfile(music_path) and os.path.isfile(illustration_path):  # 歌曲音频和曲绘图片有效
            ch = easygui.ynbox(f'是否确认以下信息？\n\n曲名：{title}\n曲师：{composer}\n画师：{illustrator}\n歌曲音频：{music_path}\n曲绘图片：{illustration_path}', '导出 ZIP 文件', ('确认', '更改'))
            if ch is None:  # 关闭对话框
                return
            elif ch:  # 选择“是”
                skip = True
        else:
            easygui.msgbox('模板中的部分文件路径已经失效，需要重新选择。', '导出 ZIP 文件', '好的')

    if not skip:
        data = (title, composer, illustrator)  # 默认信息，可能来自于模板
        while True:
            data = easygui.multenterbox('请输入歌曲信息：', '导出 ZIP 文件', ['曲名', '曲师', '画师'], data)
            if data is None:  # 关闭对话框
                return
            if not all(data):  # 存在空字符串
                easygui.msgbox('请将歌曲信息填写完整！', '导出 ZIP 文件', '哦~')
            else:
                title, composer, illustrator = data
                break

        music_path = easygui.fileopenbox('请选择歌曲音频', '导出 ZIP 文件', music_path)
        if music_path is None:
            return
        illustration_path = easygui.fileopenbox('请选择曲绘图片', '导出 ZIP 文件', illustration_path)
        if illustration_path is None:
            return

    while True:
        if len(charts_info) >= 1:  # 至少添加一张谱面
            # key 为谱面的显示名称，value 为谱面信息
            show_charts = {f'{i["difficulty"]} {i["diff_number"]} By {i["writer"]} ({i["json_path"]})': i for i in charts_info}
            ch = easygui.buttonbox(f'已添加 {len(charts_info)} 张谱面：\n'+'\n'.join(show_charts.keys()), '导出 ZIP 文件', ('继续添加', '完成添加', '删除谱面'))
            if ch is None:  # 关闭对话框
                return

            elif ch == '完成添加':
                # 保存或更新模板
                new_data = music_path, illustration_path, title, composer, illustrator, charts_info
                if using_template:
                    if easygui.ynbox('是否更新模板？', '导出 ZIP 文件', ('是', '否')):
                        # 将信息保存到原有文件中
                        json.dump(new_data, open(template_path, 'w', encoding='utf-8'), indent=4)
                        easygui.msgbox('模板更新成功！', '导出 ZIP 文件', '好耶')
                else:
                    if easygui.ynbox('是否保存模板供以后使用？', '导出 ZIP 文件', ('是', '否')):
                        template_path = easygui.filesavebox('保存模板', '导出 ZIP 文件', title+'.tpl')
                        if template_path is None:  # 未选择文件
                            return
                        json.dump(new_data, open(template_path, 'w', encoding='utf-8'), indent=4)
                        easygui.msgbox('模板保存成功！', '导出 ZIP 文件', '好耶')

                # 保存 ZIP 文件
                zip_path = easygui.filesavebox('保存 ZIP 文件', default=title+'.zip')
                if zip_path is None:  # 未保存文件
                    return
                write_zip(music_path, illustration_path, title, composer, illustrator, charts_info, zip_path)
                easygui.msgbox('导出成功！', '导出 ZIP 文件', '好耶')
                return

            elif ch == '删除谱面':
                charts_to_delete = easygui.multchoicebox('请选择要删除的谱面（支持多选）', '导出 ZIP 文件', show_charts.keys())
                for chart in charts_to_delete:
                    charts_info.remove(show_charts[chart])
                continue

        data = ('', '', '')
        while True:
            data = easygui.multenterbox(f'请输入第 {len(charts_info)+1} 张谱面信息：', '导出 ZIP 文件', ['难度', '定数', '谱师'], data)
            if data is None:  # 关闭对话框
                if len(charts_info) >= 1:
                    break  # 回到谱面列表
                else:
                    return
            if not all(data):  # 存在空字符串
                easygui.msgbox('请将谱面信息填写完整！', '导出 ZIP 文件', '哦~')
            else:
                difficulty, diff_number, writer = data
                break

        if data is None:
            continue  # 回到谱面列表

        json_path = easygui.fileopenbox('请选择谱面工程文件', '导出 ZIP 文件', '*.json')
        if json_path is None:
            continue  # 回到谱面列表
        charts_info.append({'difficulty': difficulty, 'diff_number': diff_number, 'writer': writer, 'json_path': json_path})
