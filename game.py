"""
    The class that creates an instance of the game.
    It is what manages the players and the map.
"""

# Importing the application's modules
import player
import global_map


class Game:

    #---------- CONSTRUCTOR ----------
    def __init__(self, n_players=1, map=None):

        # set the global map
        self.global_map = GlobalMap() if not map else map

        self.players = []
        for i in range(n_players): self.players.append(Player(i))
