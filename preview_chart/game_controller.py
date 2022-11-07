import time

import pygame

from constants import *
from .window_controller import Window


class Game:
    def __init__(self, omgc_data: tuple, game_window: Window) -> None:
        self.lines, self.notes, self.commands = omgc_data
        self.game_window = game_window
        self.start_time = time.time()+1  # 游戏时间从 -1 开始
        self.current_notes = []
        self.event_processor = {
            PLAY_MUSIC:         self.play_music,
            ACTIVATE_NOTE:      self.activate_note,
            REMOVE_NOTE:        self.remove_note,
            NOTE_POS:           self.note_pos,
            NOTE_TRACK_LINEAR:  self.note_track_linear,
            NOTE_TRACK_SINE:    self.note_track_sine,
            LINE_ALPHA_LINEAR:  self.line_alpha_linear,
            LINE_ALPHA_SINE:    self.line_alpha_sine,
            LINE_POS_LINEAR:    self.line_pos_linear,
            LINE_POS_SINE:      self.line_pos_sine
        }

    def main_loop(self) -> None:
        while True:
            game_time = time.time()-self.start_time
            while len(self.commands) >= 1 and self.commands[0][0] < game_time:
                event = self.commands.pop(0)
                self.event_processor[event[1]](*event[2])

            self.game_window.start_drawing()

            if self.game_window.end_drawing():
                break

    def play_music(self) -> None:
        pass

    def activate_note(self, note_id: int) -> None:
        pass

    def remove_note(self, note_id: int) -> None:
        pass

    def note_pos(self, note_id: int, a: float, b: float, c: float) -> None:
        pass

    def note_track_linear(self, note_id: int, k: float, b: float) -> None:
        pass

    def note_track_sine(self, note_id: int, a: float, o: float, p: float, b: float) -> None:
        pass

    def line_alpha_linear(self, line_id: int, k: float, b: float) -> None:
        pass

    def line_alpha_sine(self, line_id: int, a: float, o: float, p: float, b: float) -> None:
        pass

    def line_pos_linear(self, line_id: int, k: float, b: float) -> None:
        pass

    def line_pos_sine(self, line_id: int, a: float, o: float, p: float, b: float) -> None:
        pass
