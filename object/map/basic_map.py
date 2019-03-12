
import object.map.grid as grid
import object.map.tile as tile
import view.transform as transform

# ----- Parameters -----
TILE_COLORS = {
    "DEFAULT": (1.0, 0.0, 0.0, 1.0),
    "HOVER": (0.5, 0.5, 0.5, 1.0),
    "ON": (0.2, 0.5, 1.0, 1.0)
}

class BasicMap:

    def __init__(self, _radius):

        self.radius = _radius
        self.tiles = self.generate_tiles()
        # self.grid = grid.Grid(radius)

        self.selected_tile = None
        self.show_info = False

    def __del__(self):
        del self.tiles

    def generate_tiles(self):
        """Generate an array of tile in a hexagonal shape.

        -------
        Returns:
            array: list
        """
        array = []
        try:
            for q in range(-self.radius,self.radius+1):

                r1 = max(-self.radius, -q - self.radius)
                r2 = min(self.radius, -q + self.radius)

                for r in range(r1,r2+1):
                    hex_posisiton = (q, r)
                    array.append(
                        tile.Tile(hex_posisiton, TILE_COLORS)
                        )
        except Exception as e:
            print("An error has occurred while generating the map: " + str(e))
        else:
            if self.show_info:
                print('Successfully generated a map of %i tile(s).' % len(array))
        finally:
            return array


    def draw(self, projection_view_matrix, shaders):
        for tile in self.tiles:
            tile.draw(projection_view_matrix, shaders)

    def get_tile(self, _hex_position):
        for tile in self.tiles:
            if tile.position == _hex_position:
                return tile

        return None

    def set_entity(self, _hex_position, entity):
        tile = self.get_tile(_hex_position)
        if tile:
            tile.set_entity(entity)


    def update_mouse(self, mouse_hex_round, clicks):
        for tile in self.tiles:
            if tile.position[0] == mouse_hex_round[0] and tile.position[1] == mouse_hex_round[1]:
                tile.hover = True
                if clicks.get("left", False):
                    self.select(tile)
            else:
                if tile.hover:
                    tile.hover = False

        if self.selected_tile and self.selected_tile.entity and self.get_tile(mouse_hex_round) != None:
            if clicks.get("right", False) and not self.selected_tile.entity.is_moving:
                # Get the entity of the current selected tile
                current_entity = self.selected_tile.entity
                current_entity.move(self.selected_tile.position, mouse_hex_round)
                # Remove the entity
                self.selected_tile.remove_entity()

                # Get the new tile position
                new_tile = self.get_tile(mouse_hex_round)
                self.select(new_tile)               # select it
                new_tile.set_entity(current_entity) # set the entity

    def update_map_pointer(self, _dt, keys):
        if self.selected_tile:
            action = self.selected_tile.update(_dt, keys)
            return action

    def select(self, _tile):
        try:
            for tile in self.tiles:
                    tile.selected = False

            _tile.selected = True
            self.selected_tile = _tile
        except:
            print("Can't select this tile ...")
