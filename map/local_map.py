"""
    =- L O C A L   M A P -=
"""

from map.global_map import HexagonalTile

class Map:

    #---------- CONSTRUCTOR ----------------
    def __init__(self, global_map):
        self.global_map = global_map

        self.viewable_objects = []
        self.viewable_tiles = []
        self.VIEW_COLOR = (1.0, 1.0, 0.0, 1.0)

    #---------- METHODS --------------------
    def draw(self, projection_view_matrix, shaders):
        for tile in self.viewable_tiles:
            tile.draw(projection_view_matrix, shaders["color"])

        for object in self.viewable_objects:
            object.draw(projection_view_matrix, shaders["texture"])


    def update(self, id):
        self.viewable_objects = self.global_map.get_player_objects(id)

        self.viewable_tiles = []
        for object in self.viewable_objects:
            pos = object.hex_position
            hex_tile = HexagonalTile(pos[0], pos[1], self.VIEW_COLOR)
            hex_tile.set_y(0.03)
            self.viewable_tiles.append(hex_tile)
