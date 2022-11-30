import easygui

from Core.file_io import read_json
from .object_loader import load_objects
from .line import handle_line
from .note import handle_note


def main() -> None:
    """
    编辑特效
    """
    if file_path := easygui.fileopenbox('打开工程文件', default='*.mtmlproj'):
        project_data = read_json(file_path)
        while True:
            objects = load_objects(project_data['line_list'])
            if (choice := easygui.choicebox('请选择操作对象', '编辑特效', sorted(objects.keys()))) is None:
                break
            obj = objects[choice]
            if 'note_list' in obj:  # 判定线
                handle_line(obj)
            else:  # 音符
                handle_note(obj)
