from . import convert_8k_to_4k, edit_effect, manual_export, open_file, open_folder


def get_scripts() -> dict:
    """
    获取脚本
    返回：name-function dict
    """
    return {
        '打开文件': open_file.main,
        '打开文件夹': open_folder.main,
        '编辑特效': edit_effect.main,
        '手动导出': manual_export.main,
        '8K 转双面 4K': convert_8k_to_4k.main
    }
