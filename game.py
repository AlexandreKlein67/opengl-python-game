"""
    The class that creates an instance of the game.
    It is what manages the players and the map.
"""

# Importing the application's modules
import player
from map.global_ import Map


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

    #---------- METHODS --------------------
    def draw(self, projection_view_matrix, shaders):
        """
        Params :
        projection_view_matrix : mat4
            -> The matrix to project the map
        shaders : dict
            -> Both shaders ("texture" & "color")
        """

        # Get the app player and draw his local map
        self.get_player(self.app_player_id).draw(projection_view_matrix, shaders)

        # Draw the global map
        # NOTE: It only needs the color shader
        self.global_map.draw(projection_view_matrix, shaders["color"])


    #---------- GETTERS & SETTERS ----------
    def get_player(self, n):
        for player in self.players:
            if player.id == n:
                return player

        # If not find, return the first
        return self.players[0]
