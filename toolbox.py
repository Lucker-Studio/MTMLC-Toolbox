import traceback

import easygui

builtin_modules = {
    '导入谱面': 'import_chart',
    '导出谱面': 'export_chart',
    '预览谱面': 'preview_chart'
}
title = 'MTMLC-Toolbox v1.0 Alpha'

if __name__ == '__main__':
    while ch := easygui.choicebox('请选择要使用的功能', title, builtin_modules.keys()):
        try:
            __import__(builtin_modules[ch]).main()
        except Exception:
            traceback.print_exc()
            easygui.exceptionbox(f'使用功能“{ch}”时出错', title)
