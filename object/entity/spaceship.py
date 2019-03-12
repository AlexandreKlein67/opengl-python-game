
from object.entity.entity import Entity

from object.entity.building import Colony

class SpaceShip(Entity):

    def __init__(self):
        super().__init__("res/models/default.obj", "res/textures/default_tex.png", True)


class Builder(Entity):

    def __init__(self):
        super().__init__("res/models/default.obj", "res/textures/default_tex.png", True)

        self.set_action(key='c')

        def build_colony(self, tile):
            if not tile.building:
                tile.building = Colony()
