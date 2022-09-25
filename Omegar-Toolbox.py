import easygui

import export_omgz
import import_malody

TITLE = 'Omegar Toolbox v0.1.220925'

builtin_functions = {
    '导入 Malody 谱面': import_malody.main,
    '导出 OMGZ 文件': export_omgz.main
}

if __name__ == '__main__':
    while True:
        ch = easygui.choicebox('请选择要使用的功能', TITLE, builtin_functions.keys())
        if not ch:
            break
        try:
            builtin_functions[ch]()
        except:
            easygui.exceptionbox(f'使用功能“{ch}”时出错！', TITLE)
