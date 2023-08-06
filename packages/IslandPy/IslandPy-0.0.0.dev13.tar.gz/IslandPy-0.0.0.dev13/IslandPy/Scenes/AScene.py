import traceback
from abc import ABC

import pygame


class AScene(ABC):
    __slots__ = ("name", "objects", "prev_scene", "next_scenes", "window")

    def __init__(self, name: str, prev_scene: "AScene" = None) -> None:
        self.name = name
        self.objects = []
        self.prev_scene = prev_scene
        self.next_scenes = dict()
        self.window = None

    def on_scene_change(self) -> None:
        pass

    def on_scene_started(self) -> None:
        pass

    def change_scene(self, name: str) -> None:
        try:
            scene = self.next_scenes[name]
        except KeyError:
            traceback.print_exc()
            return

        scene.prev_scene = self
        scene.next_scenes[self.name] = self
        if not scene.window:
            scene.window = self.window
        self.on_scene_change()
        self.window.change_scene(scene)
        scene.on_scene_started()

    def update(self, dt) -> None:
        [o.update(dt) for o in self.objects]

    def draw(self, surface: pygame.Surface) -> None:
        [o.draw(surface) for o in self.objects]

    def handle_events(self, event: pygame.event.Event) -> None:
        [o.handle_events(event) for o in self.objects]
