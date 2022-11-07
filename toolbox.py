import easygui

import export_zip
import import_malody
import preview_chart
from constants import *

builtin_modules = {
    '导入 Malody 谱面': import_malody,
    '导出 ZIP 文件': export_zip,
    '谱面预览': preview_chart
}

if __name__ == '__main__':
    while ch := easygui.choicebox('请选择要使用的功能', TOOLBOX_TITLE, builtin_modules.keys()):
        try:
            builtin_modules[ch].main()
        except:
            easygui.exceptionbox(f'使用功能“{ch}”时出错！', TOOLBOX_TITLE)
