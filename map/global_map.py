"""
    =- G L O B A L   M A P -=
    It has all the positions, the entities and informations.
    It then gives the infos to the local maps as they ask them.
"""

# Import function and constants from libraries
from random import randint
from math import radians, cos, sin
from OpenGL.GL import GL_LINE_LOOP

import numpy as np

# Import application's modules
from object.mesh import Mesh
from view.transform import hex_to_cartesian, hex_round

class HexagonalTile(Mesh):

    #---------- CONSTRUCTOR ----------------
    def __init__(self, q=0, r=0, color=(0.5, 0.5, 0.5, 1.0)):
        """
            Create the mesh for an hexagonal tile
        """
        self.hex_position = (q, r)
        self.color = color

        # Mesh
        vertices = []

        # Create the vertices and put them in an array
        for i in range(6):
            angle_deg = 60 * i - 30
            angle_rad = radians(angle_deg)
            vertices.extend((cos(angle_rad), 0, sin(angle_rad)))

        vertices = np.array(vertices, np.float32)   # Numpy format float32

        outline_indices = np.array((
            0, 5, 4, 3, 2, 1
        ), np.uint32)

        # Create the Mesh
        super().__init__(vertices, outline_indices)

        # Set the tile at the correct position
        cartesian_position = hex_to_cartesian(self.hex_position)
        self.set_position(cartesian_position[0], 0, cartesian_position[1])

    #---------- METHODS --------------------
    def draw(self, projection_view_matrix, color_shader):
        # Set the color
        color_shader.bind()
        color_shader.set_color(self.color)
        # Draw it
        super().draw(projection_view_matrix, color_shader, draw_mod=GL_LINE_LOOP)

    #---------- GETTERS & SETTERS ----------
    def set_y(self, y):
        cartesian_position = hex_to_cartesian(self.hex_position)
        self.set_position(cartesian_position[0], y, cartesian_position[1])


class Cursor(HexagonalTile):

    #---------- CONSTRUCTOR ----------------
    def __init__(self, q, r, color):
        super().__init__(q, r, color)

        self.z_index = 0.1


class Map:

    #----------- CONSTRUCTOR ---------------
    def __init__(self, size=-1):

        MIN_SIZE = 3
        MAX_SIZE = 8

        if size < 0:
            self.size = randint(MIN_SIZE, MAX_SIZE) # Set to a random value
        else:
            self.size = size

        self.game_objects = []      # List of all the game objects
        self.hexagonal_tiles = []   # List of the tiles
        # Fill the list
        for q in range(-self.size, self.size+1):
            r1 = max(-self.size, -q - self.size)
            r2 = min(self.size, -q + self.size)
            for r in range(r1, r2+1):
                self.hexagonal_tiles.append(HexagonalTile(q, r, (0.2, 0.2, 0.2, 1.0)))

        self.cursor = Cursor(0, 0, (1.0, 0.0, 0.3, 1.0))


    #---------- METHODS --------------------
    def draw(self, projection_view_matrix, color_shader):
        # Draw each tiles
        for tile in self.hexagonal_tiles:
            tile.draw(projection_view_matrix, color_shader)

        self.cursor.draw(projection_view_matrix, color_shader)

    def update(self, mouse_hex_pos):
        # hex_mouse_pos = hex_round(mouse_pos)
        cartesian_position = hex_to_cartesian(mouse_hex_pos)
        self.cursor.set_position(cartesian_position[0], self.cursor.z_index, cartesian_position[1])


    #---------- GETTERS & SETTERS ----------
    def get_tile_objects(self, q, r):
        # Go through the list and return all objects that have the same coords
        # NOTE: The objects might not be at the hex_position because of moving
        buffer = []
        for object in self.game_objects:
            if object.hex_position == (q, r):
                buffer.append(object)

        return buffer

    def get_player_objects(self, player_id):
        # Go through the list and return all object that belong to the player
        buffer = []
        for object in self.game_objects:
            if object.player_id == player_id:
                buffer.append(object)

        return buffer

    def get_random_tile_pos(self):
        # Return a random tile position
        random_number = randint(0, len(self.hexagonal_tiles) - 1)
        tile = self.hexagonal_tiles[random_number]
        return tile.hex_position

    def is_tile_empty(self, q, r):
        # Check if the tile is empty or not
        objects = self.get_tile_objects(q, r)
        return True if len(objects) == 0 else False
