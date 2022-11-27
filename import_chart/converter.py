from common import *


def mc2mtmlproj(mc_data: dict) -> tuple:
    """
    将 Malody 谱面数据转换为工程文件数据
    返回值：song_info, chart_info, project_data
    """
    song_info = {}
    if title := mc_data['meta']['song'].get('title'):
        song_info['title'] = title
    if composer := mc_data['meta']['song'].get('artist'):
        song_info['composer'] = composer
    if illustration_file := mc_data['meta'].get('background'):
        song_info['illustration_file'] = illustration_file
    if not (difficulty := mc_data['meta'].get('version')):
        difficulty = 'Default'
    if not (writer := mc_data['meta'].get('creator')):
        writer = 'Unknown'
    chart_info = {'difficulty': difficulty,'writer': writer}
    project_data = {}
    project_data['bpm_list'] = sorted((i['beat'], i['bpm']) for i in mc_data['time'])
    line = {}

    speed_changes = sorted([(i['beat'], 'base', i['bpm']) for i in mc_data['time']] +  # 以 BPM 为基准流速
                           [(i['beat'], 'rate', i['scroll']) for i in mc_data.get('effect', [])
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
        speed_changes_processed[tuple(i[0])] = cur_base*cur_rate*MC_SPEED_RATE
    speed_changes_processed = sorted(speed_changes_processed.items(), key=lambda x: x[0][0]+x[0][1]/x[0][2])
    line['speed_changes'] = speed_changes_processed

    note_list = []
    for i in mc_data['note']:
        if 'sound' in i:
            song_info['music_file'] = i['sound']
            project_data['music_offset'] = i.get('offset', 0)/1000
        elif 'column' in i:
            note_data = {}
            note_data['start'] = i['beat']
            if 'endbeat' in i:
                note_data['end'] = i['endbeat']
            note_data['judging_track'] = i['column']
            note_list.append(note_data)

    assert len(note_list) >= 1

    line['note_list'] = note_list
    project_data['line_list'] = [line]

    return song_info, chart_info, project_data
