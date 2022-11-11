import easygui

from constants import *

builtin_modules = {
    '导入谱面': 'import_chart',
    '导出谱面': 'export_chart',
    '预览谱面': 'preview_chart'
}

if __name__ == '__main__':
    while ch := easygui.choicebox('请选择要使用的功能', DIALOG_TITLE, builtin_modules.keys()):
        try:
            __import__(builtin_modules[ch]).main()
        except Exception:
            easygui.exceptionbox(f'使用功能“{ch}”时出错！', DIALOG_TITLE)
