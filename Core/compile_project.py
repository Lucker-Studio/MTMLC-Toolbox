import math

from .common import (CHART_FRAME_HEIGHT, DEFAULT_LINE_INITIAL_ALPHA,
                     DEFAULT_LINE_INITIAL_POSITION, NOTE_PROPERTIES,
                     SLOW_MOVING_LINEAR, SLOW_MOVING_SINE)
from .common.mtmlc_commands import *


def compile_project(project_data: dict) -> tuple:
    """
    编译工程文件
    返回：lines, notes, commands（未展开）
    """

    lines = []  # 判定线列表
    notes = []  # 音符列表
    commands = []  # 指令列表

    music_offset = project_data['music_offset']
    if music_offset < 0:
        commands.append((0.0, CMD_PLAY_MUSIC, (-float(music_offset),)))
    else:
        commands.append((music_offset, CMD_PLAY_MUSIC, (0.0,)))

    beat_spb = sorted((i[0]+i[1]/i[2], 60/j) for i, j in project_data['bpm_list'])  # 节拍、每拍秒数
    beat_time_spb = [(0, 0, beat_spb[0][1])]  # 节拍、时间（s）、每拍秒数
    i = 1
    while i < len(beat_spb):
        # 计算上一个 BPM 时间点后经过的秒数
        beat_time_spb.append((beat_spb[i][0], beat_time_spb[i-1][1]+(beat_spb[i][0]-beat_spb[i-1][0])*beat_spb[i-1][1], beat_spb[i][1]))
        i += 1

    def beat2sec(beat: list) -> float:
        """
        将拍数转换为秒数
        """
        if beat is None:
            return None
        beat = beat[0]+beat[1]/beat[2]
        i = 0
        # 找到上一个 BPM 时间点
        while i+1 < len(beat_time_spb) and beat_time_spb[i+1][0] <= beat:
            i += 1
        return float(beat_time_spb[i][1]+beat_time_spb[i][2]*(beat-beat_time_spb[i][0]))

    def process_changes(initial_val: int, changes: list, linear_cmd_type: int, sine_cmd_type: int, *id) -> list:
        """
        处理缓动
        返回：指令列表
        """
        ret = []
        changes_processed = {}
        cur_val = initial_val
        for change in changes:
            t_0 = beat2sec(change['start'])  # 初时间
            t_1 = beat2sec(change.get('end', change['start']))  # 末时间
            val_0 = cur_val  # 初值
            val_1 = cur_val = change['target']  # 末值
            moving_type = change['type']
            # 必须保证缓动参数为 float 类型，而 Python 3 中 “/” 运算符返回 float 类型
            if t_0 != t_1:  # 若相等则为瞬时事件
                if moving_type == SLOW_MOVING_LINEAR:  # 线性缓动
                    k = (val_1-val_0)/(t_1-t_0)
                    b = (t_1*val_0-t_0*val_1)/(t_1-t_0)
                    changes_processed[t_0] = (moving_type, k, b)
                elif moving_type == SLOW_MOVING_SINE:  # 正弦缓动
                    A = (val_1-val_0)/2
                    o = math.pi/(t_1-t_0)
                    p = -o*(t_0+t_1)/2
                    b = (val_0+val_1)/2
                    changes_processed[t_0] = (moving_type, A, o, p, b)
            changes_processed[t_1] = (SLOW_MOVING_LINEAR, 0.0, float(val_1))
        for time, change in sorted(changes_processed.items()):
            change_type = {
                SLOW_MOVING_LINEAR: linear_cmd_type,
                SLOW_MOVING_SINE: sine_cmd_type
            }[change[0]]
            ret.append((float(time), change_type, (*id, *change[1:])))
        return ret

    for line_id, line in enumerate(project_data['line_list']):
        initial_position = float(line.get('initial_position', DEFAULT_LINE_INITIAL_POSITION))
        initial_alpha = float(line.get('initial_alpha', DEFAULT_LINE_INITIAL_ALPHA))
        commands.extend(process_changes(initial_position, line.get('motions', []), CMD_LINE_POS_LINEAR, CMD_LINE_POS_SINE, line_id))
        commands.extend(process_changes(initial_alpha, line.get('alpha_changes', []),  CMD_LINE_ALPHA_LINEAR, CMD_LINE_ALPHA_SINE, line_id))
        speed_changes = sorted((beat2sec(i), float(j)) for i, j in line['speed_changes'])
        lines.append((initial_position, initial_alpha, speed_changes[0][1]))
        cur_play_pos = 0  # 当前 line 播放位置
        play_pos_changes = [(0, speed_changes[0][1], 0)]
        for i in range(1, len(speed_changes)):
            t, k = speed_changes[i]
            cur_play_pos += play_pos_changes[-1][1]*(t-play_pos_changes[-1][0])
            b = float(cur_play_pos-t*k)
            play_pos_changes.append((t, k, b))
            commands.append((t, CMD_LINE_PLAY_POS, (line_id, k, b)))

        for note in line['note_list']:
            appear_time = beat2sec(note.get('appear'))  # 出现秒数
            start_time = beat2sec(note['start'])  # 判定秒数
            end_time = beat2sec(note.get('end', note['start']))  # 结束秒数

            def get_play_pos(t: float) -> float:
                """
                获取某一时间的播放位置
                """
                k, b = [i[1:] for i in play_pos_changes if t >= i[0]][-1]
                return k*t+b

            showing_pos_offset = get_play_pos(start_time)
            showing_length = get_play_pos(end_time)-showing_pos_offset
            initial_activated = appear_time is None and abs(showing_pos_offset) <= CHART_FRAME_HEIGHT  # note 初始可能可见

            note_data = [None]*10  # 初始化长度为 10 的数组（最后一个元素用于临时存储指令）
            note_data[0] = float(start_time)  # 起始时间
            note_data[1] = float(end_time)  # 终止时间
            note_data[2] = int(note['judging_track'])  # 判定轨道
            note_data[3] = float(initial_showing_track := note.get('initial_showing_track', note['judging_track']))  # 初始显示轨道
            note_data[4] = float(showing_pos_offset)  # 显示位置偏移
            note_data[5] = float(showing_length)  # 显示长度
            note_data[6] = line_id
            note_data[7] = int(sum(1 << i for i, j in enumerate(NOTE_PROPERTIES) if note.get('properties', {}).get(j, False)))  # 用 2 的整数次幂表示 note 的属性
            note_data[8] = int(initial_activated)  # 初始是否激活
            note_data[9] = process_changes(initial_showing_track, note.get('showing_track_changes', []), CMD_NOTE_TRACK_LINEAR, CMD_NOTE_TRACK_SINE)

            if not initial_activated:
                if appear_time is None:
                    def solve(val: float, t0: float, t1: float, k: float, b: float) -> float:
                        """
                        获取一元一次方程在区间内的解
                        """
                        if k != 0:
                            x = (val-b+showing_pos_offset)/k
                            if t0 <= x <= t1:
                                return x
                        return math.inf
                    initial_activated = False
                    for i in range(len(play_pos_changes)):
                        t0, k, b = play_pos_changes[i]
                        t1 = play_pos_changes[i+1][0] if i+1 < len(play_pos_changes) else math.inf
                        t = min(solve(CHART_FRAME_HEIGHT, t0, t1, k, b), solve(-CHART_FRAME_HEIGHT, t0, t1, k, b))  # 更早经过哪边就是从哪边出现
                        if t != math.inf:
                            note_data[9].append((float(t), CMD_ACTIVATE_NOTE, ()))
                            break
                else:
                    note_data[9].append((float(appear_time), CMD_ACTIVATE_NOTE, ()))

            notes.append(note_data)

    notes.sort()  # 按开始时间排序
    for note_id, note in enumerate(notes):
        commands.extend(map(lambda x: (x[0], x[1], (int(note_id), *x[2])), note.pop()))
    commands.sort()  # 按执行时间排序

    return lines, notes, commands
