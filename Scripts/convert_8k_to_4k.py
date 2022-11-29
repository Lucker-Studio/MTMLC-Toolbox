import os
from copy import deepcopy

import easygui

from Core.file_io import read_json, save_file, write_json

# 目标轨道数
TARGET_NUMBER_OF_TRACKS = 4


def main() -> None:
    """
    将 8K 谱面转换为双面下落 4K
    """
    if file_path := easygui.fileopenbox('打开工程文件', default='*.mtmlproj'):
        project_data = read_json(file_path)
        new_line_list = []
        for line in project_data['line_list']:
            new_line_up = deepcopy(line)
            new_line_down = deepcopy(line)
            new_line_up['note_list'] = []
            new_line_down['note_list'] = []
            for change in new_line_down['speed_changes']:
                change[1] *= -1  # 反向
            for note in line['note_list']:
                if note['judging_track'] >= TARGET_NUMBER_OF_TRACKS:
                    note['judging_track'] %= TARGET_NUMBER_OF_TRACKS
                    if 'showing_track_changes' in note:
                        for change in note['showing_track_changes']:
                            change['target'] %= TARGET_NUMBER_OF_TRACKS
                    new_line_down['note_list'].append(note)
                else:
                    new_line_up['note_list'].append(note)
            new_line_list.append(new_line_up)
            new_line_list.append(new_line_down)
        project_data['line_list'] = new_line_list
        if new_file_path := save_file('保存工程文件', '.mtmlproj', os.path.splitext(file_path)[0]+'_4K'):
            write_json(project_data, new_file_path)
            easygui.msgbox('转换成功！', '8K 转双面 4K', '好的')
