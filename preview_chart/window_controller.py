import pygame

from constants import *


class Window:
    def __init__(self, title: str, bgimg_path: str) -> None:
        pygame.init()
        self.width = FRAME_WIDTH//2
        self.height = FRAME_HEIGHT//2
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
        self.bgimg = pygame.transform.scale(pygame.image.load(bgimg_path), (self.width, self.height))

    def start_drawing(self) -> None:
        self.screen.blit(self.bgimg)

    def end_drawing(self) -> None:
        pygame.display.update()
