import easygui


def open_folder() -> None:
    """
    打开文件夹
    """
    if folder_path := easygui.diropenbox('打开文件夹'):
        pass
