import time

import pygame

from constants import *

from .func import *
from .window_controller import Window


class Game:
    def __init__(self, omgc_data: tuple, mp3_path: str, game_window: Window, note_speed_rate: float, music_volume: float) -> None:
        self.lines, self.notes, self.commands = omgc_data
        self.game_window = game_window
        self.note_speed_rate = note_speed_rate
        self.game_time = -BUFFER_TIME
        self.start_time = 0  # 游戏开始的绝对时间
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        pygame.mixer.music.set_volume(music_volume**2.5)  # Pygame 的速度曲线有点离谱
        pygame.mixer.music.load(mp3_path)
        self.activated_notes_id = [[]]*PREVIEW_TRACK_NUMBER
        self.cmd_processor = {
            CMD_PLAY_MUSIC:         self.play_music,
            CMD_ACTIVATE_NOTE:      self.activate_node,
            CMD_REMOVE_NOTE:        self.remove_note,
            CMD_NOTE_POS:           self.note_pos,
            CMD_NOTE_TRACK_LINEAR:  self.note_track_linear,
            CMD_NOTE_TRACK_SINE:    self.note_track_sine,
            CMD_LINE_ALPHA_LINEAR:  self.line_alpha_linear,
            CMD_LINE_ALPHA_SINE:    self.line_alpha_sine,
            CMD_LINE_POS_LINEAR:    self.line_pos_linear,
            CMD_LINE_POS_SINE:      self.line_pos_sine
        }

    def main_loop(self) -> None:
        """
        游戏主循环
        """
        self.start_time = time.time()-self.game_time
        while True:
            self.game_time = time.time()-self.start_time
            while len(self.commands) >= 1 and self.commands[0][0] < self.game_time:
                cmd = self.commands.pop(0)
                self.cmd_processor[cmd[1]](*cmd[2])

            self.game_window.start_drawing()

            for line in self.lines:
                self.game_window.draw_line(line.get_position(self.game_time), line.get_alpha(self.game_time))

            for track_notes in self.activated_notes_id:
                for note_id in track_notes:
                    note = self.notes[note_id]
                    self.game_window.draw_note(note.line.get_position(self.game_time)+self.note_speed_rate*note.get_position(self.game_time), self.note_speed_rate*note.showing_length, note.get_showing_track(self.game_time))

            self.game_window.end_drawing()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.quit()
                    return
                elif event.type == pygame.USEREVENT:  # 音乐结束
                    pygame.mixer.music.unload()
                    self.show_score()
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause()
                    else:
                        for track, key in enumerate(PREVIEW_KEY_MAP):
                            if event == key:
                                self.beat_track(track)
                                break
                elif event.type == pygame.KEYUP:
                    for track, key in enumerate(PREVIEW_KEY_MAP):
                        if event == key:
                            self.release_track(track)
                            break

    def pause(self) -> None:
        """
        暂停游戏
        """
        pass

    def beat_track(self, track: int) -> None:
        """
        击打判定
        """
        pass

    def release_track(self, track: int) -> None:
        """
        松开判定
        """
        pass

    def beat_note(self, note_id: int) -> None:
        """
        击打 note
        """
        pass

    def show_score(self) -> None:
        """
        结算页面
        """
        pass

    def play_music(self) -> None:
        """
        播放音乐
        """
        pygame.mixer.music.play()

    def activate_node(self, note_id: int) -> None:
        """
        激活 note
        """
        self.activated_notes_id[self.notes[note_id].judging_track].append(note_id)

    def remove_note(self, note_id: int) -> None:
        """
        移除 note
        """
        if note_id in self.activated_notes_id[self.notes[note_id].judging_track]:
            self.combo = 0
            self.activated_notes_id[self.notes[note_id].judging_track].remove(note_id)

    def note_pos(self, note_id: int, a: float, b: float, c: float) -> None:
        """
        note 位置
        """
        self.notes[note_id].get_relative_position = Quadratic_func(a, b, c)

    def note_track_linear(self, note_id: int, k: float, b: float) -> None:
        """
        note 轨道-线性
        """
        self.notes[note_id].get_showing_track = Linear_func(k, b)

    def note_track_sine(self, note_id: int, A: float, o: float, p: float, b: float) -> None:
        """
        note 轨道-正弦
        """
        self.notes[note_id].get_showing_track = Sine_func(A, o, p, b)

    def line_alpha_linear(self, line_id: int, k: float, b: float) -> None:
        """
        line 透明度-线性
        """
        self.lines[line_id].get_alpha = Linear_func(k, b)

    def line_alpha_sine(self, line_id: int, A: float, o: float, p: float, b: float) -> None:
        """
        line 透明度-正弦
        """
        self.lines[line_id].get_alpha = Sine_func(A, o, p, b)

    def line_pos_linear(self, line_id: int, k: float, b: float) -> None:
        """
        line 位置-线性
        """
        self.lines[line_id].get_position = Linear_func(k, b)

    def line_pos_sine(self, line_id: int, A: float, o: float, p: float, b: float) -> None:
        """
        line 位置-正弦
        """
        self.lines[line_id].get_position = Sine_func(A, o, p, b)
