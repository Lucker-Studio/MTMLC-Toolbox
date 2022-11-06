import pygame

from constants import *


class Window:
    """
    窗口
    """

    def __init__(self, title: str, bgimg_path: str) -> None:
        pygame.init()
        self.width = TRACK_WIDTH*4
        self.height = WINDOW_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
        self.bgimg = pygame.transform.scale(pygame.image.load(bgimg_path), (self.width, self.height))
        self.key_binding = {}
        self.key_release_binding = {}

    def add_key_binding(self, key: int, command) -> None:
        """
        添加按键绑定
        """
        self.key_binding[key] = command

    def add_key_release_binding(self, key: int, command) -> None:
        """
        添加按键释放绑定
        """
        self.key_release_binding[key] = command

    def start_drawing(self) -> None:
        """
        开始绘制帧时调用此函数
        """
        self.screen.blit(self.bgimg, (0, 0))

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
