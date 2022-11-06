import pygame


class Player:
    """
    音乐播放器
    """

    def __init__(self) -> None:
        try:
            pygame.mixer.init()
            self.playable = True
        except:  # 无法播放音频
            self.playable = False
        self.loaded = False  # 是否已打开文件
        self.started = False  # 是否已开始播放
        self.paused = False  # 是否处于暂停状态

    def open(self, file: str) -> None:
        """
        打开文件
        """
        if self.playable:
            pygame.mixer.music.load(file)
            self.loaded = True
            self.started = False

    def close(self) -> None:
        """
        关闭正在播放的文件
        """
        if self.playable:
            pygame.mixer.music.unload()
            self.loaded = False
            self.started = False

    def play(self) -> None:
        """
        播放
        """
        if self.playable and self.loaded:
            if self.started:
                if self.paused:
                    pygame.mixer.music.unpause()
                    self.paused = False
            else:
                pygame.mixer.music.play()
                self.started = True

    def pause(self) -> None:
        """
        暂停
        """
        if self.playable and self.started:
            pygame.mixer.music.pause()
            self.paused = True

    def stop(self) -> None:
        """
        停止
        """
        if self.playable and self.started:
            pygame.mixer.music.stop()
            self.started = False
            self.paused = False

    def set_pos(self, pos: float) -> None:
        """
        设置播放位置 (单位:秒)
        """
        if self.playable and pos >= 0:
            if not self.started:
                self.play()
                self.pause()
            pygame.mixer.music.set_pos(pos)
