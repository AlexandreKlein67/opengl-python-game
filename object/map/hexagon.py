import numpy as np

from math import cos, sin, radians
from OpenGL.GL import *

from view.transform import *

from object.mesh import Mesh


def construct_hexagon():
    """The function that construct the vertices of the hexagon from the center"""
    vertices = list()
    # Create the vertices and put them in an array
    for i in range(6):
        angle_deg = 60 * i - 30
        angle_rad = radians(angle_deg)
        vertices.extend((cos(angle_rad), 0, sin(angle_rad)))

    # return the list
    return np.array(vertices, np.float32)

class Hexagon(Mesh):

    def __init__(self, center, colors):

        self.colors = colors
        vertices = construct_hexagon()

        outline_indices = np.array((
            0, 5, 4, 3, 2, 1
        ), np.uint32)

        fill_indices = np.array((
            0, 5, 4,
            0, 4, 3,
            0, 3, 2,
            0, 2, 1
        ), np.uint32)

        super().__init__(vertices)
        self.add_index_buffer("outline_indices", outline_indices)
        self.add_index_buffer("fill_indices", fill_indices)

        # ---- instance variables
        self.center = center
        cartesian_position = hex_to_cartesian(self.center)
        self.set_position(cartesian_position[0], 0, cartesian_position[1])

        self.selected = False
        self.hovered = False

    def draw(self, pv_mat, shader, states):
        shader.bind()
        if states["ON"]:
            shader.set_color(self.colors["ON"])
        elif states["HOVER"]:
            shader.set_color(self.colors["HOVER"])
        else:
            shader.set_color(self.colors["DEFAULT"])

        if states["ON"] or states["HOVER"]:
            super().draw(pv_mat, shader, index_buffer_name="fill_indices")
        else:
            super().draw(pv_mat, shader, index_buffer_name="outline_indices", draw_mod=GL_LINE_LOOP)
