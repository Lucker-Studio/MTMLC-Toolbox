import easygui

import export_zip
import import_malody
from constants import *

builtin_functions = {
    '导入 Malody 谱面': import_malody.main,
    '导出 ZIP 文件': export_zip.main
}

if __name__ == '__main__':
    while ch := easygui.choicebox('请选择要使用的功能', TITLE, builtin_functions.keys()):
        try:
            builtin_functions[str(ch)]()
        except:
            easygui.exceptionbox(f'使用功能“{ch}”时出错！', TITLE)
