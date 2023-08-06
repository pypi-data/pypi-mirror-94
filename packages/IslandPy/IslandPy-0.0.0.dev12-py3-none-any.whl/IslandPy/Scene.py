from abc import ABC

import pygame


class Scene(ABC):
    def __init__(self, name: str) -> None:
        self.name = name
        self.objects = []

    def update(self, dt) -> None:
        [o.update(dt) for o in self.objects]

    def draw(self, surface: pygame.Surface) -> None:
        [o.draw(surface) for o in self.objects]

    def handle_events(self, event: pygame.event.Event) -> None:
        [o.handle_events(event) for o in self.objects]
