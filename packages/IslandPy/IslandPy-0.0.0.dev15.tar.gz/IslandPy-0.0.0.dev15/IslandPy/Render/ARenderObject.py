from typing import Tuple

import pygame
from abc import ABC
from pygame.rect import Rect

from IslandPy.Scenes.AScene import AScene


class ARenderObject(ABC):
    __slots__ = ("__is_draw", "scene", "rect", "_parent", "show_bounds", "_collision_rect", "_collision_color")

    def __init__(self, scene: AScene, size: Tuple[int, int], position: Tuple[int, int] = (0, 0)) -> None:
        pygame.init()
        self.__is_draw = True
        self.scene = scene
        self.scene.objects.append(self)
        self._parent = None
        self.rect = Rect((position[0], position[1], size[0], size[1]))
        self._collision_rect = self.rect
        self._collision_color = (255, 0, 0)
        self.show_bounds = False

    @property
    def collision_rect(self) -> pygame.Rect:
        return self._collision_rect

    @property
    def parent(self) -> "ARenderObject":
        return self._parent

    @parent.setter
    def parent(self, p: "ARenderObject") -> None:
        self._parent = p
        self.scene = p.scene

    @property
    def is_draw(self) -> bool:
        return self.__is_draw

    @property
    def x(self) -> int:
        return self.rect.x

    @property
    def y(self) -> int:
        return self.rect.y

    @property
    def width(self) -> int:
        return self.rect.width

    @property
    def height(self) -> int:
        return self.rect.height

    def get_position(self) -> Tuple[int, int]:
        return self.rect.topleft

    def set_position(self, pos: Tuple[int, int]) -> None:
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def move(self, velocity: Tuple[int, int]) -> None:
        self.rect.move_ip(velocity[0], velocity[1])

    def show(self) -> None:
        self.__is_draw = True

    def hide(self) -> None:
        self.__is_draw = False

    def update(self, dt) -> None:
        pass

    def handle_events(self, event: pygame.event.Event) -> None:
        pass

    def draw_collision(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self._collision_color, self.collision_rect, 2)

    def draw(self, surface: pygame.Surface) -> None:
        if self.show_bounds:
            self.draw_collision(surface)
