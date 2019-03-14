"""
    The class that creates an instance of the game.
    It is what manages the players and the map.
"""

# Importing the application's modules
import player
from map.global_map import Map
from game_object import *
from random import randint


class Game:

    #---------- CONSTRUCTOR ----------------
    def __init__(self, n_players=1, map=None):

        # set the global map
        self.global_map = Map() if not map else map

        # Creating the players
        self.players = []
        for i in range(n_players):
            self.players.append(player.Player(i, self.global_map))

        # Set the player that plays on this application to 0 by default
        self.app_player_id = 0

        # --- Create the map ---
        # self.create_planets()

        self.demo_create_unit()

    #---------- METHODS --------------------
    def draw(self, projection_view_matrix, shaders):
        """
        Params :
        projection_view_matrix : mat4
            -> The matrix to project the map
        shaders : dict
            -> Both shaders ("texture" & "color")
        """
        # Draw the global map
        # NOTE: It only needs the color shader
        self.global_map.draw(projection_view_matrix, shaders["color"])

        # Get the app player and draw his local map
        self.get_player(self.app_player_id).draw(projection_view_matrix, shaders)

    def create_planets(self):
        n_planets = randint(len(self.players) + 3, len(self.players) + 7)
        for i in range(n_planets):

            temp_pos = self.global_map.get_random_tile_pos()
            while not self.global_map.is_tile_empty(temp_pos[0], temp_pos[1]):
                temp_pos = self.global_map.get_random_tile_pos()

            mesh_constructor = {
                "model": "res/models/planet.obj",
                "texture": "res/textures/planet.jpg"
            }
            temp_planet = GameObject(mesh_constructor, temp_pos)
            self.global_map.game_objects.append(temp_planet)
            print("Creating a new planet at position :", temp_pos)

    def demo_create_unit(self, player_id=0):
        mesh_constructor = {
            "model": "res/models/default.obj",
            "texture": "res/textures/default_tex.png",
            "is_png": True
        }

        game_object_constructor = {
            "mesh_constructor": mesh_constructor,
            "hex_position": (0, 0)
        }

        entity_constructor = {
            "player_id": player_id
        }

        print("creating a new demo unit for player", player_id)
        temp_unit = Unit(game_object_constructor, entity_constructor)
        self.global_map.game_objects.append(temp_unit)

    def update(self, mouse_hex_pos, mouse_clicks, keys_on):
        # Update the player
        self.get_player(self.app_player_id).update(mouse_clicks)

        # Update the global map
        self.global_map.update(mouse_hex_pos)

    #---------- GETTERS & SETTERS ----------
    def get_player(self, n):
        for player in self.players:
            if player.id == n:
                return player

        # If not find, return the first
        return self.players[0]
