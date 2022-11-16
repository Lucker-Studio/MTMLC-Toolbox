import time

import PIL.Image
import PIL.ImageFilter
import pygame

from common import *


class Window:
    """
    窗口
    """

    def __init__(self, title: str, bgimg_path: str, num_of_tracks: int) -> None:
        pygame.init()
        self.num_of_tracks = num_of_tracks
        self.width = PREVIEW_TRACK_WIDTH*self.num_of_tracks+PREVIEW_SPLIT_WIDTH*(self.num_of_tracks+1)
        self.height = PREVIEW_WINDOW_HEIGHT
        self.rate = self.height/CHART_FRAME_HEIGHT
        self.size = self.width, self.height

        bgimg_original = PIL.Image.open(bgimg_path)
        bgimg_resized = bgimg_original.resize(self.size)  # 缩放大小
        bgimg_dark = bgimg_resized.point(lambda x: x*PREVIEW_BACKGROUND_BRIGHTNESS)  # 降低亮度
        bgimg_blur = bgimg_dark.filter(PIL.ImageFilter.GaussianBlur(PREVIEW_BACKGROUND_BLUR))  # 高斯模糊
        self.bgimg = pygame.image.frombuffer(bgimg_blur.tobytes(), self.size, bgimg_blur.mode)
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), PREVIEW_FONT_SIZE)

        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(title)

        if DEBUG_MODE:
            self.frame_count = 0
            self.fps = '?'
            self.last_time = time.time()

    def start_drawing(self, music_progress: float) -> None:
        """
        开始绘制帧时调用此函数
        """
        self.screen.blit(self.bgimg, (0, 0))
        for i in range(self.num_of_tracks+1):  # 绘制分割线
            rect_split_line = pygame.Rect(i*(PREVIEW_TRACK_WIDTH+PREVIEW_SPLIT_WIDTH), 0, PREVIEW_SPLIT_WIDTH, self.height)
            pygame.draw.rect(self.screen, PREVIEW_SPLIT_COLOR, rect_split_line)
        rect_progress_line = pygame.Rect(0, 0, self.width*music_progress, PREVIEW_PROGRESS_WIDTH)
        pygame.draw.rect(self.screen, PREVIEW_PROGRESS_COLOR, rect_progress_line)  # 绘制进度条

    def draw_line(self, pos: float, alpha: float) -> None:
        """
        绘制判定线
        """
        surf_line = pygame.Surface((self.width, PREVIEW_LINE_WIDTH), pygame.SRCALPHA)
        surf_line.fill((*PREVIEW_LINE_COLOR, int(alpha*255)))
        rect_line = surf_line.get_rect()
        rect_line.centery = pos*self.rate
        self.screen.blit(surf_line, rect_line)

    def draw_note(self, pos: float, length: float, track: float, alpha: float) -> None:
        """
        绘制音符
        """
        real_pos_x = (PREVIEW_TRACK_WIDTH+PREVIEW_SPLIT_WIDTH)*track+PREVIEW_SPLIT_WIDTH+PREVIEW_TRACK_WIDTH/2
        real_pos_y = pos*self.rate
        rect_note = pygame.Rect((0, 0), (PREVIEW_NOTE_WIDTH, length*self.rate))
        rect_note.midbottom = (real_pos_x, real_pos_y)
        if rect_note.height < 0:
            rect_note.height *= -1
            rect_note.top -= rect_note.height
        rect_note.top -= PREVIEW_NOTE_HEIGHT/2
        rect_note.height += PREVIEW_NOTE_HEIGHT
        surf_note = pygame.Surface(rect_note.size, pygame.SRCALPHA)
        pygame.draw.rect(surf_note, (*PREVIEW_NOTE_COLOR, int(alpha*255)), pygame.Rect((0, 0), rect_note.size), border_radius=PREVIEW_NOTE_BORDER_RADIUS)
        self.screen.blit(surf_note, rect_note)

    def end_drawing(self) -> None:
        """
        完成绘制帧时调用此函数
        """
        if DEBUG_MODE:
            now_time = time.time()
            if now_time-self.last_time >= PREVIEW_FPS_UPDATE_TIME:
                self.fps = str(round(self.frame_count/PREVIEW_FPS_UPDATE_TIME))
                self.last_time = now_time
                self.frame_count = 1
            else:
                self.frame_count += 1
            text_fps = self.font.render(self.fps, True, PREVIEW_FONT_COLOR)
            rect_fps = text_fps.get_rect()
            rect_fps.bottomright = self.size
            self.screen.blit(text_fps, rect_fps)

        pygame.display.update()  # 更新画面
