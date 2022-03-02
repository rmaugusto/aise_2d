from typing import Optional
from xmlrpc.client import boolean
import arcade
import pymunk
from ai.ai import Ai, Brain
from sensor import Sensor, SensorSet
from context import AiseContext
from entity import AiSpriteEntity, SpriteEntity
from plugin import GenericPlugin
import random


class FishPlugin(GenericPlugin):

    GROUP_FISH = 'fish'

    def __init__(self, aise_context: AiseContext):
        super().__init__(aise_context)
        self.aise_context.groups[FishPlugin.GROUP_FISH] = 8
        self.fish_list = arcade.SpriteList()
        self.points = []
        self.ai = None
        self.fish_textures = []

    def setup(self):

        self.ai = Ai(self.aise_context.config.plugins.fish.ai_function,
                     self.aise_context.config.plugins.fish.ai_mode)


        self.fish_textures.append(arcade.load_texture(
            "assets/sprites/fish.png", 0, 0, 96, 96))
        self.fish_textures.append(arcade.load_texture(
            "assets/sprites/fish.png", 96, 0, 96, 96))
        self.fish_textures.append(arcade.load_texture(
            "assets/sprites/fish.png", 192, 0, 96, 96))

        self.create_fishes()

        self.aise_context.physics_engine.add_collision_handler(
            self.aise_context.groups[AiseContext.GROUP_GROUND], self.aise_context.groups[FishPlugin.GROUP_FISH], post_handler=self.fish_hit_ground_handler)
        self.aise_context.physics_engine.add_collision_handler(
            self.aise_context.groups[FishPlugin.GROUP_FISH], self.aise_context.groups[FishPlugin.GROUP_FISH], post_handler=self.fish_hit_fish_handler)

    def create_fishes(self):

        locations_available = list(
            range(0, len(self.aise_context.map_cache.water_sprites)))
        random.shuffle(locations_available)

        for i in range(0, self.aise_context.config.plugins.fish.count):
            water_ref = self.aise_context.map_cache.water_sprites[locations_available.pop(
            )]
            fish_sprite = Fish(
                sensor_count=self.aise_context.config.plugins.fish.sensor_count,
                brain=self.ai.create_brain()
            )
            fish_sprite.id = i
            fish_sprite.brain.id = i
            fish_sprite.brain.active = True
            fish_sprite.textures = self.fish_textures
            fish_sprite.center_x = water_ref.center_x
            fish_sprite.center_y = water_ref.center_y
            fish_sprite.set_texture(0)
            fish_sprite.turn_left(random.randint(0, 360))
            fish_sprite.sensor_set.attach_space(
                self.aise_context.physics_engine.space)

            self.aise_context.physics_engine.add_sprite(fish_sprite,
                                                        friction=0.0,
                                                        body_type=pymunk.Body.DYNAMIC,
                                                        collision_type=self.aise_context.groups[
                                                            FishPlugin.GROUP_FISH]
                                                        )

            self.aise_context.physics_engine.get_physics_object(fish_sprite).shape.filter = pymunk.ShapeFilter(
                categories=self.aise_context.groups[FishPlugin.GROUP_FISH], mask=0b1001)

            self.fish_list.append(fish_sprite)

        self.ai.begin_generation( [ f.brain for f in self.fish_list ]  )

    def fish_hit_fish_handler(self, sprite_a, sprite_b, arbiter, space, data):
        self.aise_context.remove_sprite_lazy(sprite_a)
        self.aise_context.remove_sprite_lazy(sprite_b)
        sprite_a.brain.active = False
        sprite_b.brain.active = False
        self.validate_generation()

    def fish_hit_ground_handler(self, sprite_a, sprite_b, arbiter, space, data):
        fish = sprite_a if isinstance(sprite_a, Fish) else sprite_b
        fish.brain.active = False
        self.aise_context.remove_sprite_lazy(fish)
        self.validate_generation()

    def validate_generation(self):
        if len(self.fish_list) - len(self.aise_context.sprites_to_remove) <= 0:
            self.ai.end_generation()
            self.create_fishes()

    def init(self):
        pass

    def update(self, delta_time):
        self.fish_list.update()
        self.fish_list.update_animation(delta_time)

        for fish in self.fish_list:
            fish.move_forward(self.aise_context)

        self.collect_best_fishes()

    def collect_best_fishes(self):
        # get 4 best fishes according to traveled distance
        best_fishes = []
        for fish in self.fish_list:
            if len(best_fishes) < 4:
                best_fishes.append(fish)
            else:
                best_fishes.sort(key=lambda x: x.travelled)
                if fish.travelled > best_fishes[0].travelled:
                    best_fishes[0] = fish

        for i, fish in enumerate(best_fishes):
            self.aise_context.data_panel.add_label(
                '#'+str(i)+': ' + str(fish.travelled))

    def draw(self):
        self.fish_list.draw()

        for fish in self.fish_list:
            fish.sensor_set.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT:
            for fish in self.fish_list:
                fish.turn_right(20)
                fo = self.aise_context.physics_engine.get_physics_object(fish)
                fo.body.angle = fish.radians

        elif key == arcade.key.LEFT:
            for fish in self.fish_list:
                fish.turn_left(20)
                fo = self.aise_context.physics_engine.get_physics_object(fish)
                fo.body.angle = fish.radians


class Fish(AiSpriteEntity):
    def __init__(self, sensor_count: int, brain: Brain):
        super().__init__(scale=0.4, brain=brain)

        self.r_x = 0
        self.r_y = 0
        self.travelled = 0
        self.time_elapsed = 0
        self.direction = 1
        self.sensor_set = SensorSet(self, sensor_count)
        self.id = 0

    def update_animation(self, delta_time: float = 1 / 60):
        self.time_elapsed += delta_time

        # TODO: Variar o tempo de acordo com a velocidade
        if(self.time_elapsed >= 0.3):
            self.time_elapsed = 0

            self.cur_texture_index = self.cur_texture_index + self.direction

            if(self.cur_texture_index > 1):
                self.direction = -1
            elif(self.cur_texture_index < 1):
                self.direction = 1

            self.set_texture(self.cur_texture_index)

    def get_children(self):
        return []

    def move_forward(self, context: AiseContext):
        force = (0, context.config.plugins.fish.speed)
        context.physics_engine.apply_force(self, force)
        self.sensor_set.update(context)
        self.travelled += force[1] / 1000
