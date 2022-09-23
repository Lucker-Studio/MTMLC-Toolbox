import json
import math

from .constants import *

print('没写完，勿使用')
raise Exception()


def read_json(json_path: str) -> list:
    """
    将 json 项目文件读取为指令列表。
    """
    project_data = json.load(open(json_path))  # 读取 json 数据
    instructions = []  # 谱面指令列表
    beats = []  # 节拍对应的秒数
    bpm_list = sorted((i[0]+i[1]/i[2], j) for i, j in project_data['bpm_list'])
    last_time = bpm_list[0][0]  # 上一个 BPM 时间点
    i = 1

    def beat2sec(beat: list) -> float:
        """
        将拍数转换为秒数。
        """
        beat = beat[0]+beat[1]/beat[2]
        beat -= 1
        if int(beat) == beat:
            beat = int(beat)
        if beat < 0:
            # 根据开头两拍确定的直线计算
            return (beats[1]-beats[0])*beat+beats[0]
        elif beat > len(beats)-1:
            # 根据结尾两拍确定的直线计算
            return (beats[-1]-beats[-2])*(beat-len(beats)+1)+beats[-1]
        elif type(beat) == int:
            # 直接作为下标获取
            return beats[beat]
        else:
            # 根据前后两拍确定的直线计算
            last_beat = math.floor(beat)
            next_beat = math.ceil(beat)
            return beats[last_beat]*(next_beat-beat)+beats[next_beat]*(beat-last_beat)

    def process_changes(initial_val: int, changes: list, include_first: bool = False) -> dict:
        """
        处理缓动。
        """
        changes_processed = {}
        if include_first:
            changes_processed[0] = (LINEAR_SLOW_MOVING, 0, initial_val)
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
                elif moving_type == SIN_SLOW_MOVING:  # 正弦缓动
                    A = (val_0-val_1)/2
                    o = math.pi/(t_0-t_1)
                    p = o*(t_0+t_1)/2
                    b = (val_0+val_1)/2
                    changes_processed[t_0] = (moving_type, A, o, p, b)
            changes_processed[t_1] = (LINEAR_SLOW_MOVING, 0, val_1)
        return changes_processed

    for note in project_data['note_list']:
        start_time = beat2sec(note['start'])  # 判定秒数
        end_time = beat2sec(note['end'])  # 结束秒数
        key_points = list((beat2sec(i), j) for i, j in note['speed_key_points'])  # 转换关键点列表
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
                    # 计算 note 开始时的位置以便后续计算显示长度
                    start_pos = first_two(start_time)+c
                if key_points[i][0] <= end_time < key_points[i+1][0]:  # 结束时间处于当前区间
                    # 计算 note 结束时的位置以便后续计算显示长度
                    end_pos = first_two(end_time)+c
                cur_point_pos = first_two(key_points[i+1][0])+c  # 将下一个关键点代入二次函数
        for i in range(len(key_points_abc)):
            # 使 note 判定时的位置为 0，即与判定线重合
            key_points_abc[i][-1] -= start_pos

        if abs(key_points_abc[0][-1]) <= FRAME_HEIGHT:  # note 开始就可见
            activate_time = -PREACTIVATING_TIME  # 提前激活 note
        else:
            for i in range(len(key_points_abc)-1):
                t_0, a, b, c = key_points_abc[i]
                t_1 = key_points_abc[i+1][0]

                def solve(pos):
                    """
                    解方程，返回区间内的最小解，若无解则返回 inf。
                    """
                    if b == 0:  # 不是方程
                        return math.inf
                    elif a == 0:  # 一元一次方程
                        x = (pos-c)/b
                        if t_0 <= x <= t_1:
                            return x
                    else:  # 一元二次方程
                        d = b**2-4*a*(c-pos)  # 求根判别式
                        if d >= 0:  # 在实数范围内有解
                            x_1 = (-b-math.sqrt(d))/(2*a)  # 较小的根
                            x_2 = (-b+math.sqrt(d))/(2*a)  # 较大的根
                            if t_0 <= x_1 <= t_1:
                                return x_1
                            elif t_0 <= x_2 <= t_1:
                                return x_2
                    return math.inf

                t = min(solve(FRAME_HEIGHT), solve(-FRAME_HEIGHT))  # 更早经过哪边就是从哪边出现
                if t != math.inf:
                    activate_time = t-PREACTIVATING_TIME
                    break

        instr_add = [0]*10  # 初始化长度为 10 的数组
        instr_add[0] = note['id']  # note 的 ID
        instr_add[1] = sum(1 << i for i, j in enumerate(NOTE_PROPERTIES) if note['properties'].get(j))  # 用 2 的整数次幂表示 note 的属性
        instr_add[2:5] = map(float, key_points_abc.pop(0)[1:])  # 初始位置函数
        instr_add[5] = note['initial_showing_track']  # 初始显示轨道
        instr_add[6] = note['judging_track']  # 实际判定轨道
        instr_add[7] = float(start_time)  # 开始时间
        instr_add[8] = float(end_time)  # 结束时间
        instr_add[9] = float(end_pos-start_pos)  # 显示长度
        instructions.append((-1, ADD_NOTE, *instr_add))  # 添加 note 指令

        instructions.append((activate_time, ACTIVATE_NOTE, note['id']))  # 激活 note 指令

        for t, a, b, c in key_points_abc:
            instructions.append((float(t), CHANGE_NOTE_POS, note['id'], float(a), float(b), float(c)))  # 改变 note 位置函数指令

        showing_track_changes_processed = process_changes(note['initial_showing_track'], note['showing_track_changes'])
        for t in showing_track_changes_processed:
            instructions.append((t, CHANGE_NOTE_TRACK, *showing_track_changes_processed[t]))  # 改变 note 轨道函数指令

    line_motions_processed = process_changes(project_data['line']['initial_position'], project_data['line']['motions'], True)
    for t in line_motions_processed:
        instructions.append((t, CHANGE_LINE_POS, *line_motions_processed[t]))  # 改变判定线位置函数指令

    return sorted(instructions)  # 将指令按时间排序
