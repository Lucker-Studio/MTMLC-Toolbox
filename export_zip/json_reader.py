import json
import math

from constants import *


def read_json(json_path: str) -> tuple:
    """
    将 json 项目文件读取为指令列表。
    """
    project_data = json.load(open(json_path, encoding='utf-8'))  # 读取 json 数据
    lines = []  # 判定线列表
    notes = []  # 音符列表
    commands = []  # 指令列表
    beat_spb = sorted((i[0]+i[1]/i[2], 60/j) for i, j in project_data['bpm_list'])  # 节拍、每拍秒数
    beat_time_spb = [(0, project_data['music_offset'], beat_spb[0][1])]  # 节拍、时间（s）、每拍秒数
    i = 1
    while i < len(beat_spb):
        # 计算上一个 BPM 时间点后经过的秒数
        beat_time_spb.append((beat_spb[i][0], beat_time_spb[i-1][1]+(beat_spb[i][0]-beat_spb[i-1][0])*beat_spb[i-1][1], beat_spb[i][1]))
        i += 1

    def beat2sec(beat: list) -> float:
        """
        将拍数转换为秒数。
        """
        beat = beat[0]+beat[1]/beat[2]
        i = 0
        # 找到上一个 BPM 时间点
        while i+1 < len(beat_time_spb) and beat_time_spb[i+1][0] <= beat:
            i += 1
        return beat_time_spb[i][1]+beat_time_spb[i][2]*(beat-beat_time_spb[i][0])

    global_key_points = [(beat2sec(i), j) for i, j in project_data['global_speed_key_points']]  # 转换全局关键点列表

    def process_changes(initial_val: int, changes: list, id: int, linear_cmd_type: int, sine_cmd_type: int) -> None:
        """
        处理缓动。
        """
        changes_processed = {}
        cur_val = initial_val
        for change in changes:
            t_0 = beat2sec(change['start'])  # 初时间
            t_1 = beat2sec(change['end'])  # 末时间
            val_0 = cur_val  # 初值
            val_1 = cur_val = change['target']  # 末值
            moving_type = change['type']
            if t_0 != t_1:  # 若相等则为瞬时事件
                if moving_type == LINEAR_SLOW_MOVING:  # 线性缓动
                    k = (val_1-val_0)/(t_1-t_0)
                    b = (t_1*val_0-t_0*val_1)/(t_1-t_0)
                    changes_processed[t_0] = (moving_type, k, b)
                elif moving_type == SINE_SLOW_MOVING:  # 正弦缓动
                    A = (val_0-val_1)/2
                    o = math.pi/(t_0-t_1)
                    p = o*(t_0+t_1)/2
                    b = (val_0+val_1)/2
                    changes_processed[t_0] = (moving_type, A, o, p, b)
            changes_processed[t_1] = (LINEAR_SLOW_MOVING, 0, val_1)
        for time, change in sorted(changes_processed.values()):
            change_type = {
                LINEAR_SLOW_MOVING: linear_cmd_type,
                SINE_SLOW_MOVING: sine_cmd_type
            }[change[0]]
            commands.append((time, change_type, (id, *change[1:])))

    note_id = 0
    for line_id, line in enumerate(project_data['line_list']):
        lines.append((float(line['initial_position']), float(line['initial_alpha'])))
        process_changes(line['initial_position'], line['motions'], line_id, CHANGE_LINE_POS_LINEAR, CHANGE_LINE_POS_SINE)
        process_changes(line['initial_alpha'], line['alpha_changes'], line_id, CHANGE_LINE_ALPHA_LINEAR, CHANGE_LINE_ALPHA_SINE)

        for note in line['note_list']:
            start_time = beat2sec(note['start'])  # 判定秒数
            end_time = beat2sec(note['end'])  # 结束秒数
            key_points = [(beat2sec(i), j) for i, j in note['speed_key_points']]  # 转换关键点列表
            if not note['free_from_global_speed']:  # 受全局速度影响
                key_points += global_key_points  # 合并两组关键点
            key_points.sort()
            key_points.append((math.inf, key_points[-1][1]))
            cur_point_pos = 0  # 当前关键点的 note 位置
            key_points_abc = []  # 位置函数列表

            for i in range(len(key_points)-1):  # 通过关键点计算二次函数
                if key_points[i][0] != key_points[i+1][0]:  # 若相等则为瞬时变速事件，无需处理
                    k = (key_points[i+1][1]-key_points[i][1]) / (key_points[i+1][0]-key_points[i][0])  # 速度函数斜率
                    a = k/2  # 对速度函数做不定积分
                    b = key_points[i][1]-k*key_points[i][0]  # 将当前关键点代入速度函数求解 b

                    def first_two(x: float) -> float:
                        """
                        计算二次函数前两项之和。
                        """
                        return a*x**2+b*x

                    # 将当前关键点代入二次函数求解 c
                    c = cur_point_pos-first_two(key_points[i][0])
                    key_points_abc.append([key_points[i][0], a, b, c])
                    if key_points[i][0] <= start_time < key_points[i+1][0]:  # 开始时间处于当前区间
                        # 计算 note 开始时的位置以便应用位置偏移
                        start_pos = first_two(start_time)+c
                    if key_points[i][0] <= end_time < key_points[i+1][0]:  # 结束时间处于当前区间
                        # 计算 note 结束时的位置以便计算显示长度
                        end_pos = first_two(end_time)+c
                    cur_point_pos = first_two(key_points[i+1][0])+c  # 将下一个关键点代入二次函数
            for i in range(len(key_points_abc)):
                # 使 note 判定时的位置为 0，即与判定线重合
                key_points_abc[i][-1] -= start_pos

            if 0 <= key_points_abc[0][-1] <= FRAME_HEIGHT:  # note 开始就可见
                activate_time = -BUFFER_TIME  # 提前激活 note
            else:
                for i in range(len(key_points_abc)):
                    t_0, a, b, c = key_points_abc[i]
                    t_1 = key_points_abc[i+1][0] if i+1 < len(key_points_abc) else math.inf

                    def solve(pos):
                        """
                        解方程，返回区间内的最小解，若无解则返回 inf。
                        """
                        if a != 0:  # 一元二次方程
                            d = b**2-4*a*(c-pos)  # 求根判别式
                            if d >= 0:  # 在实数范围内有解
                                x_1 = (-b-math.sqrt(d))/(2*a)  # 较小的根
                                x_2 = (-b+math.sqrt(d))/(2*a)  # 较大的根
                                if t_0 <= x_1 <= t_1:
                                    return x_1
                                elif t_0 <= x_2 <= t_1:
                                    return x_2
                        elif b != 0:  # 一元一次方程
                            x = (pos-c)/b
                            if t_0 <= x <= t_1:
                                return x
                        return math.inf

                    t = min(solve(0), solve(FRAME_HEIGHT))  # 更早经过哪边就是从哪边出现
                    if t != math.inf:
                        activate_time = t-BUFFER_TIME
                        break

            while len(key_points_abc) > 1 and key_points_abc[1][0] < activate_time:
                key_points_abc.pop(0)  # 只保留 note 激活前的最后一个位置函数

            note_data = [None]*10  # 初始化长度为 10 的数组
            note_data[0] = sum(1 << i for i, j in enumerate(NOTE_PROPERTIES) if note['properties'].get(j, False))  # 用 2 的整数次幂表示 note 的属性
            note_data[1] = line_id
            note_data[2:5] = map(float, key_points_abc.pop(0)[1:])  # 初始位置函数
            note_data[5] = int(note['initial_showing_track'])  # 初始显示轨道
            note_data[6] = int(note['judging_track'])  # 实际判定轨道
            note_data[7] = float(start_time)  # 开始时间
            note_data[8] = float(end_time)  # 结束时间
            note_data[9] = float(end_pos-start_pos)  # 显示长度
            notes.append(note_data)
            commands.append((activate_time, ACTIVATE_NOTE, (note_id,)))  # 激活 note 指令

            remove_time = end_time+BUFFER_TIME
            commands.append((remove_time, REMOVE_NOTE, (note_id,)))  # 移除 note 指令

            for t, a, b, c in key_points_abc:
                if t >= remove_time:
                    break
                commands.append((float(t), CHANGE_NOTE_POS, (note_id, float(a), float(b), float(c))))  # 改变 note 位置函数指令

            process_changes(note['initial_showing_track'], note['showing_track_changes'], note_id, CHANGE_NOTE_TRACK_LINEAR, CHANGE_NOTE_TRACK_SINE)

            note_id += 1

    return lines, notes, sorted(commands)
