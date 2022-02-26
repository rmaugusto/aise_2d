


class PluginManager:
    def __init__(self):
        self.loaded_plugins = []
        self.first_update = False

    def load_plugins(self, aise_context):
        from plugins.fish.fish import FishPlugin
        self.loaded_plugins.append(FishPlugin(aise_context))

    def setup_plugins(self):
        for plugin in self.loaded_plugins:
            plugin.setup()

    def init_plugins(self):
        for plugin in self.loaded_plugins:
            plugin.init()

    def update_plugins(self, delta_time):
        for plugin in self.loaded_plugins:
            plugin.update(delta_time)

    def draw_plugins(self):
        for plugin in self.loaded_plugins:
            plugin.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        for plugin in self.loaded_plugins:
            plugin.on_mouse_press(x, y, button, key_modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        for plugin in self.loaded_plugins:
            plugin.on_mouse_motion(x, y, dx, dy)

    def on_mouse_release(self, x, y, button, modifiers):
        for plugin in self.loaded_plugins:
            plugin.on_mouse_release(x, y, button, modifiers)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        for plugin in self.loaded_plugins:
            plugin.on_mouse_scroll(x, y, scroll_x, scroll_y)

    def on_key_press(self, key, modifiers):
        for plugin in self.loaded_plugins:
            plugin.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        for plugin in self.loaded_plugins:
            plugin.on_key_release(key, modifiers)
