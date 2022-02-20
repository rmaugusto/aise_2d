import math
from typing import List, Optional

import arcade
import pymunk

from entity import SegmentData

SENSOR_REACH = 80

class Sensor:
    def __init__(self, ref_sprite: Optional[arcade.Sprite]) -> None:
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.shape = SegmentData(self.body, [0, 0], [900, 0], 0.0)
        self.shape.collision_type = 0
        self.shape.sensor = True
        self.shape.properties["sprite"] = ref_sprite
        self.distance = 0.0

    def draw(self) -> None:
        pv1 = self.body.position + self.shape.a.rotated(self.body.angle)
        pv2 = self.body.position + self.shape.b.rotated(self.body.angle)
        arcade.draw_line(pv1.x, pv1.y, pv2.x, pv2.y, arcade.color.RED, 1)


class SensorSet:

    SENSOR_SPACE = 20

    def __init__(self, ref_sprite: Optional[arcade.Sprite]) -> None:
        self.ref_sprite = ref_sprite
        self.sensors:List[Sensor] = []

        for i in range(0, 1):
            sensor = Sensor(ref_sprite)
            sensor.body.angle = ref_sprite.angle
            self.sensors.append(sensor)

    def update(self) -> None:
        
        center_ang = self.ref_sprite.angle+90
        begin_ang = center_ang - ( (len(self.sensors)-1) * SensorSet.SENSOR_SPACE ) / 2

        for sensor in self.sensors:

            angle = math.radians(begin_ang )

            begin_ang += SensorSet.SENSOR_SPACE

            x1 = self.ref_sprite.position[0]
            y1 = self.ref_sprite.position[1]

            x2 = x1 + math.cos(angle) * SENSOR_REACH
            y2 = y1 + math.sin(angle) * SENSOR_REACH

            sensor.shape.unsafe_set_endpoints((x1,y1), (x2,y2))

    def draw(self) -> None:
        for sensor in self.sensors:
            sensor.draw()

    def attach_space(self, space:pymunk.Space):
        for sensor in self.sensors:
            space.add(sensor.body, sensor.shape)

    def remove_space(self, space:pymunk.Space):
        for sensor in self.sensors:
            space.remove(sensor.shape)
            space.remove(sensor.body)