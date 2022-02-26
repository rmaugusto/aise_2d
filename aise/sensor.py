import math
from typing import List, Optional

import arcade
import pymunk
from context import AiseContext

from entity import SegmentData

SENSOR_REACH = 80

class Sensor:
    def __init__(self, ref_sprite: Optional[arcade.Sprite]) -> None:
        self.distance = 0.0
        self.sensor_pos = pymunk.Vec2d(0, 0)
        self.sprite = ref_sprite
        self.collision_pos = None
        self.distance = SENSOR_REACH

    def draw(self) -> None:
        arcade.draw_line(self.sprite.center_x, self.sprite.center_y,
                         self.sensor_pos.x, self.sensor_pos.y, arcade.color.RED, 1)

        if self.collision_pos:
            arcade.draw_circle_filled(
                self.collision_pos.x, self.collision_pos.y, 4, arcade.color.RED)


class SensorSet:

    SENSOR_SPACE = 35

    def __init__(self, ref_sprite: Optional[arcade.Sprite], count:int = 9) -> None:
        self.ref_sprite = ref_sprite
        self.sensors: List[Sensor] = []

        for i in range(0, count):
            sensor = Sensor(ref_sprite)
            self.sensors.append(sensor)

    def update(self, aise_context: AiseContext) -> None:

        physics_sprite = aise_context.physics_engine.get_physics_object(
            self.ref_sprite)
        center_ang = self.ref_sprite.angle+90
        begin_ang = center_ang - \
            ((len(self.sensors)-1) * SensorSet.SENSOR_SPACE) / 2

        for sensor in self.sensors:

            angle = math.radians(begin_ang)

            begin_ang += SensorSet.SENSOR_SPACE

            x1 = self.ref_sprite.position[0]
            y1 = self.ref_sprite.position[1]

            x2 = x1 + math.cos(angle) * SENSOR_REACH
            y2 = y1 + math.sin(angle) * SENSOR_REACH

            sensor.sensor_pos = pymunk.Vec2d(x2, y2)

            ps = aise_context.physics_engine.space.segment_query(
                (x1, y1), (x2, y2), 1, pymunk.ShapeFilter(mask=0b1001))

            sensor.collision_pos = None
            nearest_dist = SENSOR_REACH
            
            for p in ps:
                if physics_sprite.shape != p.shape and p.alpha < nearest_dist:
                    nearest_dist = p.alpha
                    sensor.collision_pos = p.point
                    sensor.distance = nearest_dist

    def draw(self) -> None:
        for sensor in self.sensors:
            sensor.draw()

    def attach_space(self, space: pymunk.Space):
        pass

    def remove_space(self, space: pymunk.Space):
        pass
