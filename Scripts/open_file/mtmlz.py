import tempfile

import easygui

from Core.chart_previewer import preview_chart
from Core.file_io import unpack_zip


def handle_mtmlz(file_path: str) -> None:
    """
    处理 mtmlz 文件
    """
    if choice := easygui.buttonbox('请选择要对此文件执行的操作', file_path, ('预览谱面',)):
        if choice == '预览谱面':
            chart_dir = tempfile.mkdtemp()
            unpack_zip(file_path, chart_dir)
            preview_chart(chart_dir)
