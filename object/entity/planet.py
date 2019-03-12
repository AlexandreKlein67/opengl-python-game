import numpy as np

from object.mesh import Mesh, load_mesh
from object.map.basic_map import BasicMap
from view.transform import scale, map

from object.entity.spaceship import SpaceShip
from object.entity.entity import Entity
from object.map.terrain import Desert

class Planet(Entity):

    def __init__(self, _size=1):

        # map the size of the planet between 0 and 0.7
        size = map(_size, 0, 1, 0, 0.7)

        # Creating a mesh for this entity
        super().__init__("res/models/planet.obj", "res/textures/planet.jpg")
        self.mesh.scale(size)           # scale it


        size = map(size, 0, 0.7, 0, 3)  # map the map size between 0 and 3
        size = round(size)              # round it
        self.map = BasicMap(size)       # create a grid with correct size

        self.opened = False             # grid is displayed or not
        self.delay = 0.2                # delay time for activation
        self.last_time_activated = self.delay

    def update(self, _dt, keys):
        # if self.opened:
        #     self.map.update(_dt, keys)

        super().update(_dt, keys)
        self.last_time_activated += _dt
        # print(self.last_time_activated)

        if self.last_time_activated >= self.delay and keys['e']:
            # print(self.opened)
            if self.opened:
                self.opened = False
            else:
                self.opened = True

            self.last_time_activated = 0


        return self if self.opened else None



class MainPlanet(Planet):

    def __init__(self, _size):

        super().__init__(_size)
        self.map.set_entity((0, 0), SpaceShip())

        for i, tile in enumerate(self.map.tiles):
            tile.set_terrain(Desert())
