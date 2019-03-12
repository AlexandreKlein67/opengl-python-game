
import glfw
import numpy as np

from view.transform import *

class MousePicker:

    def __init__(self, camera, projection_matrix):
        self.camera = camera
        self.projection_matrix = projection_matrix
        self.view_matrix = camera.lookat()
        self.current_ray = None
        self.mouse_hex_round = vec(0, 0)

    def update(self):
        self.view_matrix = self.camera.lookat()
        self.current_ray = self.calculate_mouse_ray()
        intersection_3d = self.intersect_with_y()
        intersection_2d = vec(intersection_3d[0], intersection_3d[2])
        self.mouse_hex_round = hex_round(cartesian_to_hex(intersection_2d))

    def calculate_mouse_ray(self):
        mouse_x, mouse_y = glfw.get_cursor_pos(self.camera.window)
        normalized_coords = self.get_normalized_device_coords(mouse_x, mouse_y)
        clip_coords = vec(normalized_coords[0], normalized_coords[1], -1, 1)
        eye_coords = self.to_eye_coords(clip_coords)
        world_ray = self.to_world_coords(eye_coords)
        return world_ray

    def to_world_coords(self, eye_coords):
        inverted_view = np.linalg.inv(self.view_matrix)
        ray_world = inverted_view @ eye_coords
        mouse_ray = vec(ray_world[0], ray_world[1], ray_world[2])
        normalized(mouse_ray)
        return mouse_ray

    def to_eye_coords(self, clip_coords):
        inverted_projection = np.linalg.inv(self.projection_matrix)
        eye_coord = inverted_projection @ clip_coords
        return vec(eye_coord[0], eye_coord[1], -1, 0)

    def get_normalized_device_coords(self, mouse_x, mouse_y):
        width, height = glfw.get_window_size(self.camera.window)
        x = (2*mouse_x) / width - 1
        y = -((2*mouse_y) / height - 1)
        return vec(x, y)

    def intersect_with_y(self):
        a = self.camera.position[0]
        b = self.camera.position[1]
        c = self.camera.position[2]

        alpha = self.current_ray[0]
        beta = self.current_ray[1]
        gamma = self.current_ray[2]

        x = a - (alpha * b)/beta
        y = 0
        z = c - (gamma * b)/beta
        return vec(x, y ,z)
