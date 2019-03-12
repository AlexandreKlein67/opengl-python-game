import numpy as np
from OpenGL.GL import *

from object.mesh import Mesh



class Pyramid(Mesh):

    def __init__(self):

        vertices = np.array((
            -.5, -.5, 0.5,  #0
            0.5, -.5, 0.5,  #1
            0.5, -.5, -.5,  #2
            -.5, -.5, -.5,  #3
            0.0, 0.5, 0.0   #4
        ), np.float32)

        indices = np.array((
            0, 1, 4,
            1, 2, 4,
            2, 3, 4,
            3, 0, 4,
            0, 3, 1,
            3, 2, 1
        ), np.uint32)

        colors = np.array((
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0,
            1.0, 1.0, 0.0,
            0.0, 1.0, 1.0,

        ), np.float32)



        super().__init__(vertices, indices)
        self.add_buffer(colors, 3, 1)
