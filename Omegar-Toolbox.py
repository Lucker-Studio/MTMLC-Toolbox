import easygui

import project_exporter

TITLE = 'Omegar Toolbox v0.1.220918'

builtin_functions = {
    '将项目导出为 OMGZ 文件': project_exporter.main,
    '测试': lambda: print('Hello World!')
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
