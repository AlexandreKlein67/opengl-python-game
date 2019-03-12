
import object.map.terrain as terrain
from object.map.hexagon import Hexagon

from view.transform import hex_to_cartesian

class Tile:

    def __init__(self, _position, _colors):

        self.position = _position
        self.colors = _colors

        self.entity = None
        self.terrain = terrain.Void()
        self.layout = Hexagon(_position, _colors)

        self.hover = False
        self.selected = False

    def draw(self, projection_view_matrix, shaders):
        states = {
            "ON": self.selected,
            "HOVER": self.hover
        }

        self.layout.draw(projection_view_matrix, shaders["color"], states)

        if self.entity:
            self.entity.draw(projection_view_matrix, shaders["texture"])

        # print(self.terrain.type)
        if self.terrain.type != terrain.types["VOID"]:
            # print("hey")
            self.terrain.draw(projection_view_matrix, shaders["texture"])

    def set_entity(self, entity):
        self.entity = entity
        if not self.entity.is_moving:
            self.entity.position = self.position

    def set_terrain(self, terrain):
        self.terrain = terrain
        self.terrain.position = self.position

    def remove_entity(self):
        self.entity = None

    def update(self, _dt, keys):
        if self.entity:
            # try:
            return self.entity.update(_dt, keys)
            # except Exception as e:
            #     print("Can't update the entity : " + str(e))
