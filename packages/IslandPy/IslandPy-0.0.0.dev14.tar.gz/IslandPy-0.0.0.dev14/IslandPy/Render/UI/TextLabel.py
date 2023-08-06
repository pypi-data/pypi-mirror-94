from typing import Tuple

import pygame
from pygame.color import Color

from IslandPy.Render.ARenderObject import ARenderObject
from IslandPy.Render.UI.Indents import Indents
from IslandPy.Scenes.AScene import AScene


class TextLabel(ARenderObject):
    __slots__ = ("_font_size", "_text", "_font_name", "__padding", "_bold", "_italic", "_alpha", "color",
                 "bg_color", "can_show_bg", "_font", "_image", "__surface")

    def __init__(self, scene: AScene, font_size: int = 1, text: str = "", font_name: str = "",
                 padding: Indents = Indents(), position: Tuple[int, int] = (0, 0), bold: bool = False,
                 italic: bool = False, alpha: int = 255, color: Color = Color(255, 255, 255),
                 bg_color: Color = Color(0, 0, 0), can_show_bg: bool = False) -> None:

        super().__init__(scene=scene, size=(0, 0), position=position)
        self._alpha = alpha
        self.can_show_bg = can_show_bg
        self._font_name = font_name
        self._font_size = font_size
        self._bold = bold
        self._italic = italic
        self.font_name = font_name
        self._text = text
        self.color = color
        self.bg_color = bg_color
        self._image = None
        self.__surface = None
        self.__padding = padding
        self.padding = padding
        self.text = text

    def copy_style_from(self, other: "TextLabel") -> None:
        self.bold = other.bold
        self.italic = other.italic
        self.color = other.color
        self.bg_color = other.bg_color
        self.font_size = other.font_size
        self.font_name = other.font_name
        self.can_show_bg = other.can_show_bg
        self.padding = other.padding
        self.alpha = other.alpha

        self.text = self.text

    @property
    def padding(self) -> Indents:
        return self.__padding

    @padding.setter
    def padding(self, value: Indents) -> None:
        self.__padding = value
        self.text = self.text

    @property
    def alpha(self) -> int:
        return self._alpha

    @alpha.setter
    def alpha(self, value: int) -> None:
        self._alpha = value

    @property
    def bold(self) -> bool:
        return self._bold

    @bold.setter
    def bold(self, value: bool) -> None:
        self._bold = value
        self._update_font()

    @property
    def italic(self) -> bool:
        return self._italic

    @italic.setter
    def italic(self, value: bool) -> None:
        self._italic = value
        self._update_font()

    @property
    def font_name(self) -> str:
        return self._font_name

    @font_name.setter
    def font_name(self, value: str) -> None:
        if not value:
            self._font_name = pygame.font.get_default_font().removesuffix(".ttf")
        else:
            self._font_name = value
        self._update_font()

    @property
    def font_size(self) -> int:
        return self._font_size

    @font_size.setter
    def font_size(self, value: int) -> None:
        self._font_size = value
        self._update_font()

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value
        self._image = self._font.render(self._text, True, self.color)
        if self.can_show_bg:
            self.rect.w = self._image.get_rect().w + self.padding.right + self.padding.left
            self.rect.h = self._image.get_rect().h + self.padding.bottom + self.padding.top

            self.__surface = pygame.Surface((self.rect.w, self.rect.h))  # lgtm [py/call/wrong-arguments]
            self.__surface.fill(color=self.bg_color)
            self.__surface.blit(self._image, (self.padding.left, self.padding.top))
            self.__surface.set_alpha(self.alpha)
        else:
            self.rect.w, self.rect.h = self._image.get_rect().w, self._image.get_rect().h

    def _update_font(self):
        if self._font_name in pygame.font.get_fonts():
            self._font = pygame.font.SysFont(self._font_name, self._font_size)
        else:
            self._font = pygame.font.Font(f"{self._font_name}.ttf", self._font_size)

        self._font.set_bold(self._bold)
        self._font.set_italic(self._italic)

    def draw(self, surface: pygame.Surface) -> None:
        if not self._text or not self.is_draw:
            return

        if self.can_show_bg:
            surface.blit(self.__surface, self.rect)
        else:
            surface.blit(self._image, self.rect)
        super(TextLabel, self).draw(surface)
