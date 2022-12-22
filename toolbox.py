import easygui

import Scripts

PROGRAM_VERSION = 'v1.0.2'
PROGRAM_TITLE = f'MTMLC Toolbox {PROGRAM_VERSION}'
PROGRAM_NAME = f'Multi-track Multi-line Chart Toolbox {PROGRAM_VERSION}'


def main() -> None:
    """
    工具箱主菜单
    """
    scripts = Scripts.get_scripts()
    while choice := easygui.buttonbox(f'欢迎使用 {PROGRAM_NAME}！\n请选择要使用的功能。', PROGRAM_TITLE, list(scripts.keys())):
        try:
            scripts[choice]()
        except Exception:
            easygui.exceptionbox(f'哎呀——功能“{choice}”出错了！', PROGRAM_TITLE)


if __name__ == '__main__':
    main()
