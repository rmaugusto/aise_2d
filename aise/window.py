import collections
import time
from typing import Optional
import arcade
import arcade.gui
from pyglet.math import Vec2
from pymunk import ShapeFilter
from context import AiseContext
from arcade.gui import UIManager
from arcade.gui.widgets import UITextArea, UIInputText, UITexturePane

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Artificial Intelligence Simulated Environment"
SPRITE_SCALING_TILES = 1


class FPSCounter:
    def __init__(self):
        self.time = time.perf_counter()
        self.frame_times = collections.deque(maxlen=60)

    def tick(self):
        t1 = time.perf_counter()
        dt = t1 - self.time
        self.time = t1
        self.frame_times.append(dt)

    def get_fps(self):
        total_time = sum(self.frame_times)
        if total_time == 0:
            return 0
        else:
            return len(self.frame_times) / sum(self.frame_times)


class AiseWindow(arcade.Window):

    def __init__(self, aise_context: Optional[AiseContext] = None):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

        arcade.set_background_color(arcade.csscolor.BLACK)

        self.aise_context = aise_context

        self.mouse_down = False

        self.fps = FPSCounter()

        self.manager = arcade.gui.UIManager()

        self.manager.enable()

        self.camera_sprites = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.camera_sprites.resize(self.width, self.height)
        self.camera_gui.resize(self.width, self.height)

    def setup(self):

        self.load_map()

        config_button = arcade.gui.UIFlatButton(
            text="...", width=120, height=30, y=10, x=20, style={"bg_color": (164, 90, 82, 200)})

        self.manager.add(
            config_button
        )

        self.aise_context.plugin_manager.setup_plugins()

    def load_map(self):
        tile_map = arcade.load_tilemap(
            'assets/map/map.tmx', SPRITE_SCALING_TILES)
        self.map_list = tile_map.sprite_lists["full_map"]

        for sprite in self.map_list:
            file_name = sprite.texture.name.split('/')[-1]
            image_info = file_name.split('-')

            if(image_info[1] == '32' and image_info[2] == '64'):
                sprite.properties['tile_type'] = AiseContext.GROUP_WATER
                self.aise_context.map_cache.water_sprites.append(sprite)
            elif(image_info[1] == '0' and image_info[2] == '64'):
                sprite.properties['tile_type'] = AiseContext.GROUP_GROUND
                self.aise_context.map_cache.ground_sprites.append(sprite)

            self.aise_context.physics_engine.add_sprite(sprite,
                                                        friction=0.0,
                                                        collision_type=self.aise_context.groups[
                                                            sprite.properties['tile_type']],
                                                        body_type=arcade.PymunkPhysicsEngine.STATIC)
            self.aise_context.physics_engine.get_physics_object(sprite).shape.filter = ShapeFilter(
                categories=self.aise_context.groups[sprite.properties['tile_type']])

    def on_update(self, delta_time):
        self.aise_context.plugin_manager.update_plugins(delta_time)
        self.aise_context.physics_engine.step()

    def on_draw(self):
        self.clear()

        self.camera_sprites.use()

        self.map_list.draw()
        self.aise_context.plugin_manager.draw_plugins()
        self.aise_context.remove_pending_sprites()

        self.camera_gui.use()

        # Draw the FPS
        fps = self.fps.get_fps()
        self.aise_context.system_panel.add_label(f"FPS: {fps:3.0f}")
        self.draw_data_panel()
        self.draw_system_panel()
        self.manager.draw()
        self.fps.tick()

    def draw_data_panel(self):
        sorted_labels = dict(
            sorted(self.aise_context.data_panel.labels.items()))
        _, right, _, top = arcade.get_viewport()
        ww = right
        wh = top
        pw = 160
        ph = self.height
        pos = 0
        arcade.draw_xywh_rectangle_filled(
            ww-pw, wh-ph, pw, ph, (200, 200, 200, 130))

        for _, label in sorted_labels.items():
            arcade.draw_text(label, ww - pw + 10,
                             wh - 20 - (pos * 20), arcade.color.BLACK, 12)
            pos += 1

        self.aise_context.data_panel.clear()

    def draw_system_panel(self):
        sorted_labels = dict(
            sorted(self.aise_context.system_panel.labels.items()))
        _, right, _, top = arcade.get_viewport()
        ww = right
        wh = top
        pw = 160
        ph = self.height
        pos = 0
        arcade.draw_xywh_rectangle_filled(
            0, wh-ph, pw, ph, (200, 200, 200, 130))

        for _, label in sorted_labels.items():
            arcade.draw_text(label, 10,
                             wh - 20 - (pos * 20), arcade.color.BLACK, 12)
            pos += 1

        self.aise_context.system_panel.clear()

    def on_mouse_press(self, x, y, button, key_modifiers):
        if(key_modifiers & arcade.key.MOD_CTRL == arcade.key.MOD_CTRL and button == arcade.MOUSE_BUTTON_LEFT):
            self.mouse_down = True

        self.aise_context.plugin_manager.on_mouse_press(
            x, y, button, key_modifiers)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if(self.mouse_down):
            (cx, cy) = self.camera_sprites.position
            dx *= self.aise_context.scale * 1.5
            dy *= self.aise_context.scale * 1.5
            self.camera_sprites.move((cx - dx, cy - dy))

        self.aise_context.plugin_manager.on_mouse_motion(x, y, dx, dy)

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        self.mouse_down = False

        self.aise_context.plugin_manager.on_mouse_release(x, y, button,
                                                          modifiers)

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):

        new_scale = self.aise_context.scale + scroll_y * 0.05

        if(new_scale > 0.5 and new_scale < 3):
            self.aise_context.scale = new_scale
            self.camera_sprites.scale = new_scale

        self.aise_context.plugin_manager.on_mouse_scroll(
            x, y, scroll_x, scroll_y)

    def on_key_press(self, key, modifiers):

        self.aise_context.plugin_manager.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):

        self.aise_context.plugin_manager.on_key_release(key, modifiers)
