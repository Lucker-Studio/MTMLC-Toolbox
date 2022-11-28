from .manual_export import manual_export
from .open_file import open_file
from .open_folder import open_folder


def get_scripts() -> dict:
    """
    获取脚本
    返回：name-function dict
    """
    return {
        '打开文件': open_file,
        '打开文件夹': open_folder,
        '手动导出': manual_export
    }
