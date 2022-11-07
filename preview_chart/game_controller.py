import time

import pygame

from constants import *
from .func import *
from .window_controller import Window


class Game:
    def __init__(self, omgc_data: tuple, mp3_path: str, game_window: Window) -> None:
        self.lines, self.notes, self.commands = omgc_data
        self.game_window = game_window
        self.game_time = -1  # 游戏时间从 -1 开始
        self.start_time = time.time()-self.game_time  # 游戏开始的绝对时间
        self.combo = 0
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        pygame.mixer.music.load(mp3_path)
        self.activated_notes_id = []
        self.cmd_processor = {
            CMD_PLAY_MUSIC:         pygame.mixer.music.play,
            CMD_ACTIVATE_NOTE:      self.activated_notes_id.append,
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
        while True:
            self.game_time = time.time()-self.start_time
            while len(self.commands) >= 1 and self.commands[0][0] < self.game_time:
                cmd = self.commands.pop(0)
                self.cmd_processor[cmd[1]](*cmd[2])

            self.game_window.start_drawing()

            for line in self.lines:
                self.game_window.draw_line(line.get_position(self.game_time), line.get_alpha(self.game_time))

            for note_id in self.activated_notes_id:
                note = self.notes[note_id]
                self.game_window.draw_note(note.get_position(self.game_time), note.get_showing_track(self.game_time))

            self.game_window.end_drawing()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause()
                    else:
                        for track, key in enumerate(PREVIEW_KEY_MAP):
                            if event == key:
                                self.beat(track)
                                break
                elif event.type == pygame.KEYUP:
                    for track, key in enumerate(PREVIEW_KEY_MAP):
                        if event == key:
                            self.release(track)
                            break
                elif event.type == pygame.USEREVENT:  # 音乐结束
                    self.show_score()
                    return

    def pause(self) -> None:
        """
        暂停游戏
        """
        pass

    def beat(self, track: int) -> None:
        """
        击打判定
        """
        pass

    def release(self, track: int) -> None:
        """
        松开判定
        """
        pass

    def show_score(self) -> None:
        """
        结算页面
        """
        pass

    def remove_note(self, note_id: int) -> None:
        """
        移除 note
        """
        if note_id in self.activated_notes_id:
            self.combo = 0
            self.activated_notes_id.remove(note_id)

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
