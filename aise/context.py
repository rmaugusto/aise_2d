from typing import List
from arcade import PymunkPhysicsEngine, Sprite

from plugin_manager import PluginManager


class AiseContext:

    TILE_TYPE_GROUND = 'ground'
    TILE_TYPE_WATER = 'water'

    def __init__(self):
        self.scale = 1
        self.map_cache = MapCache()
        self.physics_engine = PymunkPhysicsEngine(damping=0,
                                            gravity=(0,0))
        self.plugin_manager = PluginManager()
        self.plugin_manager.load_plugins(self)

class MapCache:
    def __init__(self):
        self.ground_sprites: List[Sprite] = []
        self.water_sprites: List[Sprite] = []
