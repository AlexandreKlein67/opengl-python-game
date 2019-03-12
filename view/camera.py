"""
    Class to navigate in the scene
"""
# External modules
import glfw
import numpy as np
from math import cos, sin, radians

from view.transform import *

class Camera:

    def __init__(self, window):

        self.position = vec(0, 5, 3)
        self.front = vec(0, 0, -1)
        self.right = vec(1, 0, 0)
        self.up = vec(0, 1, 0)

        self.window = window


        self.target = vec(0, 0, 0)

        self.pitch = -45
        self.yaw = -90

        self.sensivity = 0.05
        self.speed = 1
        self.zoom_factor = 10
        self.zoom_speed = 50

        self.update_camera_vectors()

    def lookat(self):
        return lookat(self.position, self.front + self.position, self.up)


    def process_mouse_mouvement(self, xoffset, yoffset):

        xoffset *= self.sensivity
        yoffset *= self.sensivity

        self.position += vec(xoffset, 0, 0)
        self.position += vec(0, 0, yoffset)
        # self.pitch += yoffset
        # self.yaw += xoffset
        self.update_camera_vectors()

    def update_camera_vectors(self):
        front = vec(
            cos(radians(self.yaw)) * cos(radians(self.pitch)),
            sin(radians(self.pitch)),
            sin(radians(self.yaw)) * cos(radians(self.pitch))
        )

        self.front = normalized(front)
        self.right = normalized(np.cross(self.front, self.up))
        self.up = normalized(np.cross(self.right, self.front))
