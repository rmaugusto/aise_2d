from typing import List
from arcade import PymunkPhysicsEngine, Sprite
import yaml
from plugin_manager import PluginManager
from munch import Munch

class PanelLabel:

    def __init__(self):
        self.labels:dict[int, str] = {}

    def add_label(self, label:str):
        if len(self.labels) == 0:
            m = 0
        else:
            m = max(list(self.labels.keys())) + 1
            
        self.labels[m] = label

    def set_label(self, label:str, idx:int):
        if id in self.labels:
            raise Exception('Label already exists')

        self.labels[idx] = label

    def clear(self):
        self.labels.clear()    

class AiseContext:

    GROUP_GROUND = 'ground'
    GROUP_WATER = 'water'
    GROUP_SENSOR = 'sensor'

    def __init__(self):
        self.scale = 1
        self.groups:dict[str, int] = {}
        self.groups[AiseContext.GROUP_GROUND] = 1
        self.groups[AiseContext.GROUP_WATER] = 2
        self.groups[AiseContext.GROUP_SENSOR] = 4
        self.sprites_to_remove:List[Sprite] = []

        self.system_panel:PanelLabel = PanelLabel()
        self.data_panel:PanelLabel = PanelLabel()

        self.map_cache = MapCache()
        self.physics_engine = PymunkPhysicsEngine(damping=0,
                                            gravity=(0,0))
        self.plugin_manager = PluginManager()
        self.plugin_manager.load_plugins(self)

        for _, v in self.groups.items():
            self.physics_engine.collision_types.append( v )


        with open("config/aise.yaml", "r") as stream:
            self.config = Munch.fromDict(yaml.safe_load(stream)) 

    def remove_sprite_lazy(self, sprite):
        self.sprites_to_remove.append(sprite)

    def remove_pending_sprites(self):
        for sprite in self.sprites_to_remove:
            sprite.remove_from_sprite_lists()

        self.sprites_to_remove = []

class MapCache:
    def __init__(self):
        self.ground_sprites: List[Sprite] = []
        self.water_sprites: List[Sprite] = []
