from abc import ABC, abstractmethod

from context import AiseContext

class GenericPlugin(ABC):


    def __init__(self, aise_context: AiseContext) -> None:
        super().__init__()
        self.aise_context = aise_context

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    def on_key_release(self, key, modifiers):
        pass

    def on_key_press(self, key, modifiers):
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        pass

