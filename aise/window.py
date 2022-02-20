from typing import Optional
import arcade
from pyglet.math import Vec2
from context import AiseContext

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Artificial Intelligence Simulated Environment"
SPRITE_SCALING_TILES = 1

class AiseWindow(arcade.Window):

    def __init__(self, aise_context: Optional[AiseContext] = None):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.BLACK)

        self.aise_context = aise_context

        self.mouse_down = False


    def setup(self):

        self.aise_context.physics_engine.collision_types.append('sensor')

        tile_map = arcade.load_tilemap('assets/map/map.tmx', SPRITE_SCALING_TILES)
        self.map_list = tile_map.sprite_lists["full_map"]

        for sprite in self.map_list:
            file_name = sprite.texture.name.split('/')[-1]
            image_info = file_name.split('-')

            if(image_info[1] == '32' and image_info[2] == '64'):
                sprite.properties['tile_type'] = 'water'
                self.aise_context.map_cache.water_sprites.append(sprite)
            elif(image_info[1] == '0' and image_info[2] == '64'):
                sprite.properties['tile_type'] = 'ground'
                self.aise_context.map_cache.ground_sprites.append(sprite)

        self.aise_context.physics_engine.add_sprite_list(self.aise_context.map_cache.ground_sprites,
                                            friction=0.0,
                                            collision_type="ground",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

        for plugin in self.aise_context.plugin_manager.loaded_plugins:
            plugin.load(self.aise_context)
        


    def on_update(self, delta_time):
        self.aise_context.plugin_manager.update_plugins(delta_time)
        self.aise_context.physics_engine.step()

    def on_draw(self):
        self.clear()
        self.map_list.draw()
        self.aise_context.plugin_manager.draw_plugins()

    def on_mouse_press(self, x, y, button, key_modifiers):
        if( key_modifiers & arcade.key.MOD_CTRL == arcade.key.MOD_CTRL and button == arcade.MOUSE_BUTTON_LEFT):
            self.mouse_down = True

        self.aise_context.plugin_manager.on_mouse_press(x, y, button, key_modifiers)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if(self.mouse_down):
            vp = arcade.get_viewport()
            dx *= self.aise_context.scale 
            dy *= self.aise_context.scale
            arcade.set_viewport(vp[0] - dx, vp[1] - dx, vp[2] - dy, vp[3] - dy)

        self.aise_context.plugin_manager.on_mouse_motion(x, y, dx, dy)


    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        self.mouse_down = False

        self.aise_context.plugin_manager.on_mouse_release(x, y, button,
                         modifiers)        

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):

        new_scale = self.aise_context.scale + scroll_y * 0.05

        if(new_scale > 0.05 and new_scale < 2):
            left, right, bottom, top = arcade.get_viewport()
            scale = 1 + scroll_y * 0.05
            self.aise_context.scale = self.aise_context.scale + scroll_y * 0.05
            arcade.set_viewport(left * scale, right * scale, bottom * scale, top * scale) 

        self.aise_context.plugin_manager.on_mouse_scroll(x, y, scroll_x, scroll_y)

    def on_key_press(self, key, modifiers):

        self.aise_context.plugin_manager.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):

        self.aise_context.plugin_manager.on_key_release(key, modifiers)
