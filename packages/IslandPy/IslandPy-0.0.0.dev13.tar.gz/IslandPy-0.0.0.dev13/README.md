# IslandPy
![Python](https://img.shields.io/pypi/pyversions/IslandPy)
[![Grade](https://img.shields.io/lgtm/grade/python/github/ludwici/IslandPy)](https://lgtm.com/projects/g/ludwici/IslandPy/context:python)
[![Alerts](https://img.shields.io/lgtm/alerts/github/ludwici/IslandPy)](https://lgtm.com/projects/g/ludwici/IslandPy/alerts/?mode=list)
[![Pypi](https://img.shields.io/pypi/status/IslandPy)](https://pypi.org/project/IslandPy/)
[![Pypi](https://img.shields.io/pypi/v/IslandPy)](https://pypi.org/project/IslandPy/)
[![Pypi](https://img.shields.io/pypi/l/IslandPy)](https://pypi.org/project/IslandPy/)
![](https://img.shields.io/tokei/lines/github/ludwici/IslandPy)

### How to:
- [Add scenes to game][1]
- [Draw you custom object][2]
- [Simple TextLabel example][3]
## Add scenes to game
1. Define you scene:
```python
import pygame
from IslandPy.Render.ARenderObject import ARenderObject
from IslandPy.Scenes.AScene import AScene


class CustomScene(AScene):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.r1 = ARenderObject(self, size=(10, 50))

    def draw(self, surface: pygame.Surface) -> None:
        super(CustomScene, self).draw(surface)
        pygame.draw.rect(surface, (255, 255, 255), self.r1.rect)
```
Scene must be inherited from `AScene` - a base class of all scenes.

2. Create object and pass them to window
```python
r = RenderWindow()
s1 = CustomScene("Custom Scene")
r.start(s1)
```
You should create a scene between init `r` and `r.start`

## Draw you custom object
Create a child of `ARenderObject`
```python
from IslandPy.Render.ARenderObject import ARenderObject
from IslandPy.Scenes.AScene import AScene


class CustomRender(ARenderObject):
    def __init__(self, scene: AScene, size: (int, int)) -> None:
        super().__init__(scene, size)

```
IslandPy have two ways to next steps:
1. Create draw-method in `CustomRender`:
```python
def draw(self, surface: pygame.Surface) -> None:
    if self.is_draw:
        pygame.draw.rect(surface, (255, 255, 255), self.rect)
```
This method will be called automatically.

2. Overload draw-method in `CustomScene`:
```python
def draw(self, surface: pygame.Surface) -> None:
    super(CustomScene, self).draw(surface)
    pygame.draw.rect(surface, (255, 255, 255), self.r1.rect)
```

## Simple TextLabel example
Example of simple TextLabel, which increase count value by Space pressed. Create you `CustomScene` from [this][1] and modify:
```python
def __init__(self, name: str) -> None:
    super().__init__(name)
    self.count = 0
    self.label = TextLabel(scene=self, font_size=14, text="Count: 0")
```

Change text-value on update-method:
```python
def update(self, dt) -> None:
    super(CustomScene, self).update(dt)
    self.label.text = f"Count: {self.count}"
```

And add event handler:
```python
def handle_events(self, event: pygame.event.Event) -> None:
    super(CustomScene, self).handle_events(event)
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            self.count += 1
```

[1]: https://github.com/ludwici/IslandPy/tree/dev#add-scenes-to-game
[2]: https://github.com/ludwici/IslandPy/tree/dev#draw-you-custom-object
[3]: https://github.com/ludwici/IslandPy/tree/dev#simple-textlabel-example
