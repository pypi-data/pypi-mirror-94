import pygame

from IslandPy.Render.TestRender import TestRender
from IslandPy.Render.UI.Button import ButtonState, Button, ButtonEventType
from IslandPy.Scenes.AScene import AScene


class TestScene(AScene):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.r1 = TestRender(scene=self, size=(100, 100), position=(0, 0))
        self.r2 = TestRender(scene=self, size=(100, 100), position=(300, 120))
        self.b = Button(scene=self, size=(50, 10), state=ButtonState.NORMAL, position=(0, self.r2.rect.bottom),
                        default_image_path="res/btn.png")
        self.b.set_image_by_state(ButtonState.LOCKED, path="res/btn_lock.png")
        self.b.set_image_by_state(ButtonState.HOVERED, path="res/btn_hover.png")
        self.b.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.show()})

    def show(self) -> None:
        self.b.lock()

    def handle_events(self, event: pygame.event.Event) -> None:
        super().handle_events(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for o in self.objects:
                    o.show_bounds = True
                if self.r1.is_draw:
                    self.r1.hide()
                else:
                    self.r1.show()
