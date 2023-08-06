import pygame

from IslandPy.Render.ARenderObject import ARenderObject
from IslandPy.Scenes.AScene import AScene


class TestRender(ARenderObject):
    __slots__ = "_speed"

    def __init__(self, scene: AScene, size: (int, int), position: (int, int) = (0, 0)) -> None:
        super().__init__(scene, size, position)
        self._speed = 1

    def update(self, dt) -> None:
        if self.rect.x > 300 or self.rect.x < 0:
            self._speed = -self._speed
        self.rect.x += self._speed

    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self._speed = abs(self._speed)
            if event.key == pygame.K_a:
                self._speed *= -1

    def draw(self, surface: pygame.Surface) -> None:
        if self.is_draw:
            pygame.draw.rect(surface, (255, 255, 255), self.rect)
        super(TestRender, self).draw(surface)
