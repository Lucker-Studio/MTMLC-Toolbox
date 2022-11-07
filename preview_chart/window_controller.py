import pygame

from constants import *


class Window:
    """
    窗口
    """

    def __init__(self, title: str, bgimg_path: str) -> None:
        pygame.init()
        self.width = TRACK_WIDTH*TRACK_NUMBER+LINE_WIDTH*(TRACK_NUMBER+1)
        self.height = WINDOW_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
        self.bgimg = pygame.transform.scale(pygame.image.load(bgimg_path), (self.width, self.height))
        self.line_color = (200, 200, 200)
        self.note_color = ()
        self.key_binding = {}
        self.key_release_binding = {}
        self.add_key_binding = self.key_binding.__setitem__
        self.add_key_release_binding = self.key_release_binding.__setitem__

    def start_drawing(self) -> None:
        """
        开始绘制帧时调用此函数
        """
        self.screen.blit(self.bgimg, (0, 0))
        for i in range(TRACK_NUMBER+1):  # 绘制分割线
            split_line = pygame.Rect(i*(TRACK_WIDTH+LINE_WIDTH), 0, LINE_WIDTH, self.height)
            pygame.draw.rect(self.screen, self.line_color, split_line)

    def end_drawing(self) -> bool:
        """
        完成绘制帧时调用此函数，返回值表示是否退出游戏界面
        """
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key in self.key_binding:
                    self.key_binding[event.key]()
            elif event.type == pygame.KEYUP:
                if event.key in self.key_release_binding:
                    self.key_release_binding[event.key]()
        return False
