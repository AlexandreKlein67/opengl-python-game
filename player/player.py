
from player.ressources import Ressource

class Player:

    def __init__(self):

        self.ressources = {
        "iron": 0,
        "energy": 0,
        "money": 0
        }

        self.units = []
        self.buildings = []

        self.alive = True

    def update(self):

        # Death conditions
        if len(self.units) == 0 and len(self.buildings) == 0:
            self.alive = False
