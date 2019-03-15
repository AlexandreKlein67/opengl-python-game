"""
    =- L O C A L   M A P -=
"""

from map.global_map import HexagonalTile
from view.transform import hex_to_cartesian

class Map:

    #---------- CONSTRUCTOR ----------------
    def __init__(self, global_map):
        self.global_map = global_map

        self.viewable_objects = []
        self.viewable_tiles = []
        self.VIEW_COLOR = (1.0, 1.0, 0.0, 1.0)

        self.selected_object = None

    #---------- METHODS --------------------
    def draw(self, projection_view_matrix, shaders):
        for tile in self.viewable_tiles:
            tile.draw(projection_view_matrix, shaders["color"])

        for object in self.viewable_objects:
            object.draw(projection_view_matrix, shaders["texture"])


    def update(self, id, mouse_hex_pos, mouse_clicks):
        self.viewable_objects = self.global_map.get_player_objects(id)
        self.unselect_all()

        selected_pos = self.global_map.selected_tile.hex_position
        selected_objects = self.global_map.get_tile_objects(selected_pos[0], selected_pos[1])
        for object in selected_objects:
            self.select_object(object)

        self.viewable_tiles = []
        for object in self.viewable_objects:

            # Create the tiles that are visible
            pos = object.hex_position
            hex_tile = HexagonalTile(pos[0], pos[1], self.VIEW_COLOR)
            hex_tile.set_y(0.03)
            self.viewable_tiles.append(hex_tile)

            # Update the object
            object.update()

        # Move the entity
        if self.selected_object != None:
            if mouse_clicks.get("right", False):
                if self.global_map.is_a_tile(mouse_hex_pos[0], mouse_hex_pos[1]):
                    if not self.selected_object.is_moving:
                        self.global_map.selected_tile.hex_position = mouse_hex_pos
                        cartesian_position = hex_to_cartesian(mouse_hex_pos)
                        self.global_map.selected_tile.set_position(
                            cartesian_position[0],
                            self.global_map.selected_tile.z_index,
                            cartesian_position[1])

                    start_position = self.selected_object.hex_position
                    ending_position = mouse_hex_pos
                    self.selected_object.set_move_target(
                        start_position,
                        ending_position)




    def select_object(self, selected_object):
        self.unselect_all()
        selected_object.selected = True
        self.selected_object = selected_object

    def unselect_all(self):
        for object in self.viewable_objects:
            object.selected = False
        self.selected_object = None
