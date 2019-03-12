import numpy as np

from view.transform import translate
from object.mesh import Mesh

from OpenGL.GL import GL_FLOAT

class Background(Mesh):

    def __init__(self, n, size=10):
        vertices = np.array((
            -size, 0, -size,
            -size, 0, size,
            size, 0, size,
            size, 0, -size
        ), np.float32)

        color = np.array((
            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0
        ))

        texture = np.array((
            0.0, 0.0,
            1.0, 0.0,
            1.0, 1.0,
            0.0, 1.0
        ), np.float32)

        indices = np.array((
            0, 1, 2,
            0, 2, 3
        ), np.uint32)

        super().__init__(vertices, indices, position=(0, -3*n, -3*n))
        self.add_buffer(color, 4, 1)
        self.add_buffer(texture, 2, 2)
        self.set_texture("res/textures/background_0{}.png".format(n), rgba=True)

        # self.model = translate(0, -3*n, 0)

    def draw(self, pv, shaders):
        super().draw(pv, shaders["texture"])
