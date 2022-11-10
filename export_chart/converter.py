import math

from constants import *

if DEBUG_MODE:
    from tqdm import tqdm


def json2omgc(music_offset: float, bpm_list: list, line_list: list) -> tuple:
    """
    将工程文件数据转换为 omgc 谱面文件数据
    """

    lines = []  # 判定线列表
    notes = []  # 音符列表
    commands = []  # 指令列表
    beat_spb = sorted((i[0]+i[1]/i[2], 60/j) for i, j in bpm_list)  # 节拍、每拍秒数
    beat_time_spb = [(0, music_offset, beat_spb[0][1])]  # 节拍、时间（s）、每拍秒数
    i = 1
    while i < len(beat_spb):
        # 计算上一个 BPM 时间点后经过的秒数
        beat_time_spb.append((beat_spb[i][0], beat_time_spb[i-1][1]+(beat_spb[i][0]-beat_spb[i-1][0])*beat_spb[i-1][1], beat_spb[i][1]))
        i += 1

    def beat2sec(beat: list) -> float:
        """
        将拍数转换为秒数
        """
        beat = beat[0]+beat[1]/beat[2]
        i = 0
        # 找到上一个 BPM 时间点
        while i+1 < len(beat_time_spb) and beat_time_spb[i+1][0] <= beat:
            i += 1
        return beat_time_spb[i][1]+beat_time_spb[i][2]*(beat-beat_time_spb[i][0])

    def process_changes(initial_val: int, changes: list, linear_cmd_type: int, sine_cmd_type: int, *id) -> None:
        """
        处理缓动
        """
        ret = []
        changes_processed = {}
        cur_val = initial_val
        for change in changes:
            t_0 = beat2sec(change['start'])  # 初时间
            t_1 = beat2sec(change['end'])  # 末时间
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
            changes_processed[t_1] = (SLOW_MOVING_LINEAR, float(0), float(val_1))
        for time, change in sorted(changes_processed.items()):
            change_type = {
                SLOW_MOVING_LINEAR: linear_cmd_type,
                SLOW_MOVING_SINE: sine_cmd_type
            }[change[0]]
            ret.append((float(time), change_type, (*id, *change[1:])))
        return ret

    for line_id, line in enumerate(line_list):
        lines.append((float(line['initial_position']), float(line['initial_alpha'])))
        commands.extend(process_changes(line['initial_position'], line['motions'], CMD_LINE_POS_LINEAR, CMD_LINE_POS_SINE, line_id))
        commands.extend(process_changes(line['initial_alpha'], line['alpha_changes'],  CMD_LINE_ALPHA_LINEAR, CMD_LINE_ALPHA_SINE, line_id))
        global_speed_changes = sorted([(beat2sec(i), j) for i, j in line['global_speed_changes']], key=lambda x: x[0])

        for note in tqdm(line['note_list']) if DEBUG_MODE else line['note_list']:
            start_time = beat2sec(note['start'])  # 判定秒数
            end_time = beat2sec(note['end'])  # 结束秒数
            speed_changes = sorted([(beat2sec(i), j) for i, j in note['speed_changes']], key=lambda x: x[0]) if note['speed_changes'] else global_speed_changes
            cur_pos = 0  # 当前 note 位置
            pos_changes = []

            def in_period(t, t_0, t_1): return t_0 <= t <= t_1

            for i in range(len(speed_changes)-1):  # 通过关键点计算函数
                pos_changes.append([*speed_changes[i], cur_pos-speed_changes[i][0]*speed_changes[i][1]])
                if in_period(start_time, speed_changes[i][0], speed_changes[i+1][0]):  # 开始时间处于当前区间
                    # 计算 note 开始时的位置以便应用位置偏移
                    start_pos = pos_changes[-1][1]*start_time+pos_changes[-1][2]
                if in_period(end_time, speed_changes[i][0], speed_changes[i+1][0]):  # 结束时间处于当前区间
                    # 计算 note 结束时的位置以便计算显示长度
                    end_pos = pos_changes[-1][1]*end_time+pos_changes[-1][2]
                cur_pos = pos_changes[-1][1]*speed_changes[i+1][0]+pos_changes[-1][2]
            pos_changes.append([*speed_changes[-1], cur_pos-speed_changes[-1][0]*speed_changes[-1][1]])

            for change in pos_changes:
                # 使 note 判定时的位置为 0，即与判定线重合
                change[2] -= start_pos

            # note 在判定线上下 FRAME_HEIGHT 高度内时可能可见
            def solve(pos, t_0, t_1, k, b):
                if k != 0:
                    x = (pos-b)/k
                    if in_period(x, t_0, t_1):
                        return x
                return math.inf

            if abs(pos_changes[0][2]) <= CHART_FRAME_HEIGHT:  # note 在第一个时间点时可见
                activate_time = -BUFFER_TIME
            else:
                t = min(solve(CHART_FRAME_HEIGHT, -math.inf, *pos_changes[0]), solve(-CHART_FRAME_HEIGHT, -math.inf, *pos_changes[0]))
                if t != math.inf:  # note 在第一个时间点前可见
                    activate_time = t
                else:
                    for i in range(len(pos_changes)):
                        t_0, k, b = pos_changes[i]
                        t_1 = pos_changes[i+1][0] if i+1 < len(pos_changes) else math.inf
                        t = min(solve(CHART_FRAME_HEIGHT, t_0, t_1, k, b), solve(-CHART_FRAME_HEIGHT, t_0, t_1, k, b))  # 更早经过哪边就是从哪边出现
                        if t != math.inf:
                            activate_time = t
                            break

            while len(pos_changes) > 1 and pos_changes[1][0] < activate_time:
                pos_changes.pop(0)  # 只保留 note 激活前的最后一个位置函数

            note_data = [None]*10  # 初始化长度为 10 的数组（最后一个用于临时存储指令）
            note_data[0] = int(sum(1 << i for i, j in enumerate(NOTE_PROPERTIES) if note['properties'].get(j, False)))  # 用 2 的整数次幂表示 note 的属性
            note_data[1] = int(line_id)
            note_data[2:4] = map(float, pos_changes.pop(0)[1:])  # 初始位置函数
            note_data[4] = float(note['initial_showing_track'])  # 初始显示轨道
            note_data[5] = int(note['judging_track'])  # 实际判定轨道
            note_data[6] = float(start_time)  # 开始时间
            note_data[7] = float(end_time)  # 结束时间
            note_data[8] = float(end_pos-start_pos)  # 显示长度
            note_data[9] = []

            note_data[9].append((float(activate_time), CMD_ACTIVATE_NOTE, ()))  # 激活 note 指令

            remove_time = end_time+BUFFER_TIME
            note_data[9].append((float(remove_time), CMD_REMOVE_NOTE, ()))  # 移除 note 指令

            for t, k, b in pos_changes:
                if t > end_time:
                    break
                note_data[9].append((float(t), CMD_NOTE_POS_LINEAR, (float(k), float(b))))  # 改变 note 位置函数指令

            note_data[9].extend(process_changes(note['initial_showing_track'], note['showing_track_changes'], CMD_NOTE_TRACK_LINEAR, CMD_NOTE_TRACK_SINE))

            notes.append(note_data)

    notes.sort(key=lambda x: x[6])  # 按开始时间排序
    for note_id, note in enumerate(notes):
        commands.extend(map(lambda x: (x[0], x[1], (int(note_id), *x[2])), note.pop()))

    commands.sort()  # 按执行时间排序

    return lines, notes, commands
