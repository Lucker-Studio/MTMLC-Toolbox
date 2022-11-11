import time

import pygame

from constants import *

from .common import *
from .window_controller import Window


class Game:
    def __init__(self, lines: list, notes: list, commands: list, activated_notes: list, mp3_path: str, game_window: Window, note_speed_rate: float, music_volume: float, chart_offset: float) -> None:
        self.lines = lines
        self.notes = notes
        self.commands = commands
        self.activated_notes = activated_notes
        self.game_window = game_window
        self.note_speed_rate = note_speed_rate
        self.chart_offset = chart_offset
        self.game_time = -PREVIEW_WAIT_TIME
        self.start_time = 0  # 游戏开始的绝对时间
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        pygame.mixer.music.set_volume(music_volume**3)  # Pygame 的速度曲线有点离谱
        pygame.mixer.music.load(mp3_path)
        self.cmd_processor = {
            CMD_PLAY_MUSIC:         self.play_music,
            CMD_ACTIVATE_NOTE:      self.activate_node,
            CMD_NOTE_TRACK_LINEAR:  self.note_track_linear,
            CMD_NOTE_TRACK_SINE:    self.note_track_sine,
            CMD_LINE_ALPHA_LINEAR:  self.line_alpha_linear,
            CMD_LINE_ALPHA_SINE:    self.line_alpha_sine,
            CMD_LINE_POS_LINEAR:    self.line_pos_linear,
            CMD_LINE_POS_SINE:      self.line_pos_sine,
            CMD_LINE_PLAY_POS:      self.line_play_pos
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

            line_pos = []
            line_play_pos = []
            for line in self.lines:
                line_pos.append(line.get_position(self.game_time))
                self.game_window.draw_line(line_pos[-1], line.get_alpha(self.game_time))
                line_play_pos.append(line.get_play_position(self.game_time))

            for track_notes in self.activated_notes:
                for note_id in track_notes:
                    note = self.notes[note_id]
                    note_pos = line_pos[note.line_id]+self.note_speed_rate*(line_play_pos[note.line_id]-note.showing_position_offset)
                    self.game_window.draw_note(note_pos, self.note_speed_rate*note.showing_length, note.get_showing_track(self.game_time))

            self.game_window.end_drawing()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.quit()
                    return
                elif event.type == pygame.USEREVENT:  # 音乐结束
                    pygame.mixer.music.unload()
                    pygame.quit()
                    return

    def play_music(self, start_pos: float) -> None:
        pygame.mixer.music.play()
        pygame.mixer.music.set_pos(start_pos)

    def activate_node(self, note_id: int) -> None:
        self.activated_notes[self.notes[note_id].judging_track].append(note_id)

    def note_pos_linear(self, note_id: int, k: float, b: float) -> None:
        self.notes[note_id].get_relative_position = Linear_func(k, b)

    def note_track_linear(self, note_id: int, k: float, b: float) -> None:
        self.notes[note_id].get_showing_track = Linear_func(k, b)

    def note_track_sine(self, note_id: int, A: float, o: float, p: float, b: float) -> None:
        self.notes[note_id].get_showing_track = Sine_func(A, o, p, b)

    def line_alpha_linear(self, line_id: int, k: float, b: float) -> None:
        self.lines[line_id].get_alpha = Linear_func(k, b)

    def line_alpha_sine(self, line_id: int, A: float, o: float, p: float, b: float) -> None:
        self.lines[line_id].get_alpha = Sine_func(A, o, p, b)

    def line_pos_linear(self, line_id: int, k: float, b: float) -> None:
        self.lines[line_id].get_position = Linear_func(k, b)

    def line_pos_sine(self, line_id: int, A: float, o: float, p: float, b: float) -> None:
        self.lines[line_id].get_position = Sine_func(A, o, p, b)

    def line_play_pos(self, line_id: int, k: float, b: float) -> None:
        self.lines[line_id].get_play_position = Linear_func(k, b)
