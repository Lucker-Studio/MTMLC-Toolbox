import easygui

import export_chart
import import_chart
import preview_chart
import quick_preview
from constants import *

builtin_modules = {
    '导入谱面': import_chart,
    '导出谱面': export_chart,
    '谱面预览': preview_chart,
    '快速预览': quick_preview
}

if __name__ == '__main__':
    while ch := easygui.choicebox('请选择要使用的功能', DIALOG_TITLE, builtin_modules.keys()):
        try:
            builtin_modules[ch].main()
        except:
            easygui.exceptionbox(f'使用功能“{ch}”时出错！', DIALOG_TITLE)
