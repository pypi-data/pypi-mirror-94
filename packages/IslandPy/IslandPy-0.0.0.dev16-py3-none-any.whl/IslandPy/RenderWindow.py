import os
from typing import Tuple

import pygame
from pygame.time import Clock

from IslandPy.Scenes.AScene import AScene


class RenderWindow:
    def __init__(self, title: str = "", bg_color: Tuple[int, int, int] = (34, 34, 34)) -> None:
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.display.set_caption(title)
        self.__screen = pygame.display.set_mode((1280, 720))
        self.__clock = Clock()
        self.__bg_color = bg_color
        self.__done = False
        self.__pause = False
        self.fps = 60
        self.__current_scene = None
        self.can_set_title_by_scene = True

    def start(self, start_scene: AScene) -> None:
        self.change_scene(start_scene)
        self.__current_scene.window = self
        while not self.__done:
            self.__loop()
        self.__current_scene.on_scene_change()
        pygame.quit()

    def stop(self) -> None:
        self.__done = True

    def change_scene(self, scene) -> None:
        if self.can_set_title_by_scene:
            pygame.display.set_caption(scene.name)
        self.__current_scene = scene

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__done = True
            # if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_SPACE:
                #     self.__pause = not self.__pause

            if self.__pause:
                continue

            self.__current_scene.handle_events(event)

    def draw(self) -> None:
        self.__current_scene.draw(self.__screen)

    def update(self, dt) -> None:
        if self.__pause:
            return

        self.__current_scene.update(dt)

    def __loop(self) -> None:
        dt = self.__clock.tick(self.fps)
        self.__screen.fill(self.__bg_color)
        self.handle_events()
        self.update(dt)
        self.draw()
        pygame.display.flip()
