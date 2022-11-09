from constants import *


def malody2omegar(meta: dict, time: list, effect: list, note: list) -> dict:
    """
    将 Malody 谱面数据转换为 Omegar 工程文件数据
    """

    project_data = {}
    project_data['project_name'] = meta['song']['title']+' '+meta['version']
    project_data['bpm_list'] = sorted((i['beat'], i['bpm']) for i in time)
    project_data['line_list'] = [{'initial_position': CHART_LINE_INITIAL_POSITION, 'initial_alpha': 1, 'motions': [], 'alpha_changes': []}]

    speed_changes = sorted([(i['beat'], 'base', i['bpm']) for i in time] +  # 以 BPM 为基准流速
                           [(i['beat'], 'rate', i['scroll']) for i in effect
                            # effect 中的 scroll 表示流速倍数（见 https://www.bilibili.com/read/cv8257852/）
                           if 'scroll' in i], key=lambda x: x[0][0]+x[0][1]/x[0][2])  # 节拍为带分数表示
    speed_changes_processed = {}
    cur_base = 100
    cur_rate = 1
    for i in speed_changes:
        if i[1] == 'base':
            cur_base = i[2]
        elif i[1] == 'rate':
            cur_rate = i[2]
        speed_changes_processed[tuple(i[0])] = cur_base*cur_rate
    speed_changes_processed = sorted(speed_changes_processed.items(), key=lambda x: x[0][0]+x[0][1]/x[0][2])
    project_data['line_list'][0]['global_speed_changes'] = speed_changes_processed

    note_list = []
    for i in note:
        if 'column' in i:
            note_list.append({
                'start':                    i['beat'],
                'end':                      i.get('endbeat', i['beat']),
                'judging_track':            i['column'],
                'initial_showing_track':    i['column'],
                'showing_track_changes':    [],
                'speed_changes':         [],
                'properties':               {i: DEFAULT_PROPERTIES.get(i, False) for i in NOTE_PROPERTIES}
            })
        elif 'sound' in i:
            project_data['music_path'] = i['sound']
            project_data['music_offset'] = -i.get('offset', 0)/1000

    project_data['line_list'][0]['note_list'] = note_list

    return project_data
