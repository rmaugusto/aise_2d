from typing import List, Optional, Tuple

from arcade import Sprite, Texture
from pymunk import Body, Segment


class SpriteEntity(Sprite):
    def __init__(self, filename: str = None, scale: float = 1, image_x: float = 0, image_y: float = 0, image_width: float = 0, image_height: float = 0, center_x: float = 0, center_y: float = 0, repeat_count_x: int = 1, repeat_count_y: int = 1, flipped_horizontally: bool = False, flipped_vertically: bool = False, flipped_diagonally: bool = False, hit_box_algorithm: str = "Simple", hit_box_detail: float = 4.5, texture: Texture = None, angle: float = 0):
        super().__init__(filename, scale, image_x, image_y, image_width, image_height, center_x, center_y, repeat_count_x,
                         repeat_count_y, flipped_horizontally, flipped_vertically, flipped_diagonally, hit_box_algorithm, hit_box_detail, texture, angle)


class SegmentData(Segment):
    def __init__(self, body: Optional["Body"], a: Tuple[float, float], b: Tuple[float, float], radius: float, properties: dict[str, object] = None) -> None:
        super().__init__(body, a, b, radius)
        self.properties = properties
        if(self.properties is None):
            self.properties = {}

class CompositeSpriteEntity(Sprite):
    def __init__(self, entities: List[SpriteEntity]):
        super().__init__(None)
        self.entities = entities

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        return super().draw(filter=filter, pixelated=pixelated, blend_function=blend_function)

    def update(self):
        return super().update()

    def set_position(self, x: float, y: float):
        return super().set_position(x, y)
    
    def set_angle(self, angle: float):
        return super().set_angle(angle)

    def set_scale(self, scale: float):
        return super().set_scale(scale)

    def set_texture(self, texture: Texture):
        return super().set_texture(texture)

    def set_texture_index(self, index: int):
            return super().set_texture_index(index)

    def set_texture_region(self, x: float, y: float, width: float, height: float):
        return super().set_texture_region(x, y, width, height)

    def set_texture_size(self, width: float, height: float):
        return super().set_texture_size(width, height)

    def set_texture_alpha(self, alpha: float):
        return super().set_texture_alpha(alpha)

    def set_texture_angle(self, angle: float):
        return super().set_texture_angle(angle)

    def set_texture_flipped_horizontally(self, flipped: bool):
        return super().set_texture_flipped_horizontally(flipped)

    def set_texture_flipped_vertically(self, flipped: bool):
        return super().set_texture_flipped_vertically(flipped)

    def set_texture_flipped_diagonally(self, flipped: bool):
        return super().set_texture_flipped_diagonally(flipped)

    def set_texture_blend_function(self, blend_function: str):
        return super().set_texture_blend_function(blend_function)

    def set_texture_filter(self, filter: str):
        return super().set_texture_filter(filter)

    def set_texture_pixelated(self, pixelated: bool):
        return super().set_texture_pixelated(pixelated)

    def set_texture_repeat_count_x(self, count: int):
        return super().set_texture_repeat_count_x(count)

    def set_texture_repeat_count_y(self, count: int):
        return super().set_texture_repeat_count_y(count)

    def set_texture_hit_box_algorithm(self, algorithm: str):
        return super().set_texture_hit_box_algorithm(algorithm)

    def set_texture_hit_box_detail(self, detail: float):
        return super().set_texture_hit_box_detail(detail)
