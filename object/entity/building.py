
from object.mesh import load_mesh
from object.entity.entity import Entity

class Building(Entity):

    def __init__(self, model_file, texture_file, png):
        super().__init__(model_file, texture_file, png)

    def draw(self, projection_view_matrix, shader):
        self.mesh.draw(projection_view_matrix, shader)


class Colony(Building):

    def __init__(self):
        super().__init__("res/models/colony.obj", "res/textures/colony_tex.png", True)
