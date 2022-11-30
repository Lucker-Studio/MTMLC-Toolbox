import math


def format_beat(beat: list) -> str:
    """
    格式化拍子数输出
    """
    return f'{beat[0]}+{beat[1]}/{beat[2]}'


def calculate_beat(beat: list) -> float:
    """
    计算拍子数
    """
    return beat[0]+beat[1]/beat[2]


def load_objects(line_list: list) -> dict:
    """
    获取可添加特效的对象。
    """
    notes = []
    objects = {}
    num_of_digits_line = int(math.log10(len(line_list)-1))+1
    for line_id, line in enumerate(line_list):
        line_id_with_zero = str(line_id).zfill(num_of_digits_line)
        objects[f'判定线{line_id_with_zero} (pos={line["initial_position"]}, alpha={line["initial_alpha"]})'] = line
        for note in line['note_list']:
            notes.append((line_id_with_zero, note))
    notes.sort(key=lambda x: calculate_beat(x[1]["start"]))
    num_of_digits_note = int(math.log10(len(notes)-1))+1
    for note_id, (line_id, note) in enumerate(notes):
        objects[f'音符{str(note_id).zfill(num_of_digits_note)} (line={line_id}, track={note["judging_track"]}, start={format_beat(note["start"])}, end={format_beat(note.get("end",note["start"]))})'] = note
    return objects
