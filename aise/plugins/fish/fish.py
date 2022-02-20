import math
from typing import Optional
from xmlrpc.client import boolean
import arcade
import pymunk
from sensor import Sensor, SensorSet
from context import AiseContext
from entity import SegmentData, SpriteEntity
from plugin import GenericPlugin
import random


class FishPlugin(GenericPlugin):
    def __init__(self):
        self.aise_context = None
        self.fish_list = arcade.SpriteList()
        self.points = []

    def load(self, aise_context: Optional[AiseContext] = None):
        self.aise_context = aise_context
        self.aise_context.physics_engine.collision_types.append('fish')
        self.aise_context.physics_engine.collision_types.append('ground')

        locations_available = list(
            range(0, len(self.aise_context.map_cache.water_sprites)))
        random.shuffle(locations_available)

        fish_textures = []
        fish_textures.append(arcade.load_texture(
            "assets/sprites/fish.png", 0, 0, 96, 96))
        fish_textures.append(arcade.load_texture(
            "assets/sprites/fish.png", 96, 0, 96, 96))
        fish_textures.append(arcade.load_texture(
            "assets/sprites/fish.png", 192, 0, 96, 96))

        for i in range(0, 1):
            water_ref = self.aise_context.map_cache.water_sprites[locations_available.pop(
            )]
            fish_sprite = Fish()
            fish_sprite.textures = fish_textures
            fish_sprite.center_x = water_ref.center_x
            fish_sprite.center_y = water_ref.center_y
            fish_sprite.set_texture(0)
            fish_sprite.turn_left(random.randint(0, 360))
            fish_sprite.sensor_set.attach_space(
                self.aise_context.physics_engine.space)

            self.fish_list.append(fish_sprite)

        self.aise_context.physics_engine.add_sprite_list(self.fish_list,
                                                         friction=0.0,
                                                         body_type=pymunk.Body.DYNAMIC,
                                                         collision_type="fish"
                                                         )

        self.aise_context.physics_engine.add_collision_handler(
            "fish", "ground", post_handler=self.fish_hit_ground_handler)

        self.aise_context.physics_engine.add_collision_handler(
            "sensor", "ground", begin_handler=self.begin_sensor_hit_ground_handler, pre_handler=self.pre_sensor_hit_ground_handler,
            post_handler=self.post_sensor_hit_ground_handler)

    def begin_sensor_hit_ground_handler(self, sprite_a, sprite_b, arbiter: pymunk.Arbiter, space, data):
        return True

    def post_sensor_hit_ground_handler(self, sprite_a, sprite_b, arbiter: pymunk.Arbiter, space, data):
        return True

    def pre_sensor_hit_ground_handler(self, sprite_a, sprite_b, arbiter: pymunk.Arbiter, space, data):
        s1 = arbiter.shapes[0]
        s2 = arbiter.shapes[1]

        sensor_shape = s1 if isinstance(s1, SegmentData) else s2



        fish = sensor_shape.properties["sprite"]
        # fish_shape = self.aise_context.physics_engine.get_physics_object(
        #     fish).shape
        # dist = fish_shape.point_query(
        #     arbiter.contact_point_set.points[0].point_b)
        # print(dist.distance)
        # Define r_x with point of contact 

        # get nearst point of contact
        # for point in arbiter.contact_point_set.points:
            # dist = point.point_a.get_distance(fish.center_x, fish.center_y)
            # fish.r_x = point.point_a.x
            # fish.r_y = point.point_a.y 

        dists = []

        # dist = arbiter.contact_point_set.points[0].distance
        # fish.r_x = arbiter.contact_point_set.points[0].point_a.x
        # fish.r_y = arbiter.contact_point_set.points[0].point_a.y
        self.points = []

        # self.points.append( (s1.a.x, s1.a.y, arcade.color.RED) )
        # self.points.append( (s1.b.x, s1.b.y, arcade.color.YELLOW) )
        # self.points.append( (arbiter.normal.x, arbiter.normal.y, arcade.color.BLUE) )
        # self.points.append( (arbiter.contact_point_set.normal.x, arbiter.contact_point_set.normal.y, arcade.color.BLACK) )

        # self.points.append( (s2.a.x, s2.a.y) )
        # self.points.append( (s2.b.x, s2.b.y) )

        for point in arbiter.contact_point_set.points:
            self.points.append( (point.point_a.x, point.point_a.y, arcade.color.RED) )
            self.points.append( (point.point_b.x, point.point_b.y, arcade.color.ORANGE) )

            # dists.append(point.distance)

        # print(dists)

        # for point in arbiter.contact_point_set.points:
        #     if point.distance < dist:
        #         dist = point.distance
        #         fish.r_x = point.point_b.x
        #         fish.r_y = point.point_b.y



        for sensor in fish.sensor_set.sensors:
            if sensor.shape == sensor_shape:
                base = sensor_shape.a
                # print ( base.get_distance( arbiter.contact_point_set.points[0].point_a ) )
                # print(arbiter.contact_point_set.points[0].point_b)

        return True

    def fish_hit_ground_handler(self, sprite_a, sprite_b, arbiter, space, data):
        fish = sprite_a if isinstance(sprite_a, Fish) else sprite_b
        fish.sensor_set.remove_space(space)
        self.aise_context.physics_engine.remove_sprite(fish)
        self.fish_list.remove(fish)
        return True

    def init(self):
        pass

    def update(self, delta_time):
        self.fish_list.update()
        self.fish_list.update_animation(delta_time)

        # for fish in self.fish_list:
        #     force = (0, 4000)
        #     self.aise_context.physics_engine.apply_force(fish, force)
        #     fish.sensor_set.update()


    def draw(self):
        self.fish_list.draw()

        # if(len(self.fish_list) > 0):
        #     fish = self.fish_list[0]
        #     arcade.draw_circle_filled(fish.r_x, fish.r_y, 10, arcade.color.RED)

        for point in self.points:
            arcade.draw_circle_filled(point[0], point[1], 5, point[2])

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

        elif key == arcade.key.UP:
            for fish in self.fish_list:
                force = (0, 8000)
                self.aise_context.physics_engine.apply_force(fish, force)
                fish.sensor_set.update()



class Fish(SpriteEntity):
    def __init__(self):
        super().__init__(None, 0.4)

        self.r_x = 0
        self.r_y = 0

        self.time_elapsed = 0
        self.direction = 1
        self.sensor_set = SensorSet(self)

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
