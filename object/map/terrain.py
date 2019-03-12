
from object.mesh import load_mesh
from view.transform import hex_to_cartesian

types = {
    "VOID": 0,
    "DESERT": 1
}


class Terrain:

    def __init__(self):
        self.mesh = None
        self.position = (0, 0)

    def draw(self, projection_view_matrix, shader):
        if self.mesh:
            cartesian_position = hex_to_cartesian(self.position)
            self.mesh.set_position(cartesian_position[0], -0.1, cartesian_position[1])
            self.mesh.draw(projection_view_matrix, shader)


class Void(Terrain):

    def __init__(self):
        self.type = types["VOID"]

        super().__init__()


class Desert(Terrain):

    def __init__(self):
        super().__init__()
        self.mesh = load_mesh("res/models/hexagon.obj", "res/textures/desert_tex.png", True)

        self.type = types["DESERT"]
