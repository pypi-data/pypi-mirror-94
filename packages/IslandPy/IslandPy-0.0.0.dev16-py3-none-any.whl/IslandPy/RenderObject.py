import pygame
from pygame.rect import Rect

from IslandPy.Scenes.AScene import AScene


class RenderObject:
    def __init__(self, scene: AScene, size: (int, int), position: (int, int) = (0, 0)) -> None:
        self._speed = 1
        self._is_draw = True
        self.scene = scene
        self.scene.objects.append(self)
        self.rect = Rect((position[0], position[1], size[0], size[1]))

    @property
    def is_draw(self) -> bool:
        return self._is_draw

    def show(self) -> None:
        self._is_draw = True

    def hide(self) -> None:
        self._is_draw = False

    def update(self, dt) -> None:
        if self.rect.x > 300 or self.rect.x < 0:
            self._speed = -self._speed
        move = self._speed
        self.rect.x += move

    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self._speed = abs(self._speed)
            if event.key == pygame.K_a:
                self._speed *= -1

    def draw(self, surface: pygame.Surface) -> None:
        if self._is_draw:
            pygame.draw.rect(surface, (255, 255, 255), self.rect)
