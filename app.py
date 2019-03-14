# External modules
import glfw
from OpenGL.GL import *
import numpy as np
import math

# Internal modules

# Shaders
from shader import Shader

# View
from view.transform import *
from view.camera import *
from view.mouse_picker import MousePicker

# Meshes
from object.map.grid import Grid
from object.map.basic_map import BasicMap
from object.map.background import Background

from object.entity.planet import *

from object.test.pyramid import Pyramid
from object.mesh import Mesh, load_mesh
from object.entity.building import Colony

from game import Game

# ---------- Viewer class -----------------------------------------------------
class Viewer:

    def __init__(self, width=640, height=480, name="Window"):

        glfw.window_hint(glfw.RESIZABLE, True)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)

        self.width, self.height = width, height

        primary = glfw.get_primary_monitor()
        mode = glfw.get_video_mode(primary)

        self.win = glfw.create_window(width, height, name, None, None)
        if not self.win:
            glfw.terminate()
            exit()

        glfw.make_context_current(self.win)

        glfw.set_key_callback(self.win, self.on_key)
        glfw.set_window_size_callback(self.win, self.window_resize)
        # glfw.set_input_mode(self.win, glfw.CURSOR, glfw.CURSOR_NORMAL)
        glfw.set_cursor_pos_callback(self.win, self.on_mouse)
        glfw.set_scroll_callback(self.win, self.on_scroll)
        glfw.set_mouse_button_callback(self.win, self.on_mouse_button)

        print('OpenGL', glGetString(GL_VERSION).decode() + ', GLSL',
              glGetString(GL_SHADING_LANGUAGE_VERSION).decode() +
              ', Renderer', glGetString(GL_RENDERER).decode(), '\n')

        glClearColor(0, 0, 0, 1)
        glEnable(GL_CULL_FACE)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

        glEnable(GL_DEPTH_TEST)
        # glEnable(GL_ALPHA_TEST)
        glDepthFunc(GL_LEQUAL)
        # glDepthMask(GL_FALSE)


        self.elements = list()
        self.colored_elements = list()
        # self.colored_elements.append(Pyramid())

        self.camera = Camera(self.win)

        self.trackball = Trackball()
        winsize = glfw.get_window_size(self.win)
        self.projection = self.trackball.projection_matrix(winsize)

        self.mouse_picker = MousePicker(self.camera, self.projection)

        self.texture_shader = Shader("res/shaders/basicShader")
        self.color_shader = Shader("res/shaders/grid")
        self.shaders = {
            "color": self.color_shader,
            "texture": self.texture_shader
        }

        self.map_pointer = None
        self.keys = {
            "e": False
        }
        self.clicks = {}


        self.delta_time = 0
        self.last_frame = 0

        self.last_x = 400
        self    .last_y = 300
        self.first_mouse = True

        self.move_x = 0
        self.move_y = 0


        # self.map = BasicMap(5)
        self.game = Game()

        main_planet = MainPlanet(1.0)
        main_planet_pos = (0, 0)

        # self.map.set_entity(main_planet_pos, main_planet)
        # Trying to enter the main planet at the launch
        # self.map.selected_tile = self.map.get_tile(main_planet_pos)
        # self.map_pointer = main_planet

        # self.elements.append(self.map)

        self.elements.extend((
            Background(1, 20),
            Background(2, 20),
            Background(3, 20)))

        self.pyramid = Pyramid()

        # self.mesh = load_mesh("res/models/planet.obj", "res/textures/planet.jpg", False)
        # self.elements.append(self.mesh)


    def run(self):
        while not glfw.window_should_close(self.win):

            # ----- OpenGL functions ------------------------
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glAlphaFunc(GL_GREATER, 0)
            glfw.poll_events()

            # ----- Time ------------------------------------
            # Get the delta_time
            current_frame = glfw.get_time()
            self.delta_time = current_frame - self.last_frame
            self.last_frame = current_frame

            # ----- Mouse -----------------------------------
            self.mouse_picker.update()
            mouse_hex_round = self.mouse_picker.mouse_hex_round

            # Update the main map or the inner map if one is selected
            # if self.map_pointer:
            #     self.map_pointer.map.update_mouse(mouse_hex_round, self.clicks)
            # else:
            #     self.map.update_mouse(mouse_hex_round, self.clicks)

            # ----- Camera ----------------------------------
            self.camera.process_mouse_mouvement(self.move_x, self.move_y)
            winsize = glfw.get_window_size(self.win)
            view = self.camera.lookat()
            projection_view_matrix = self.projection @ view

            # ----- Update ----------------------------------
            self.update()

            # ----- Draw ------------------------------------
            self.draw(projection_view_matrix)

            # Swap buffers
            glfw.swap_buffers(self.win)


    def update(self):
        # self.map_pointer = self.map.update_map_pointer(self.delta_time, self.keys)

        # if self.map_pointer:
        #     for tiles in self.map_pointer.map.tiles:
        #         tiles.update(self.delta_time, self.keys)
        pass

    def draw(self, projection_view_matrix):
        # if self.map_pointer == None:
        #     for element in self.elements:
        #         element.draw(projection_view_matrix, self.shaders)
        # else:
        #     self.map_pointer.map.draw(projection_view_matrix, self.shaders)
        self.game.draw(projection_view_matrix, self.shaders)


    def on_key(self, _win, key, _scancode, action, _mods):
        """ 'Q' or 'Escape' quits """
        if action == glfw.PRESS or action == glfw.REPEAT:
            if key == glfw.KEY_ESCAPE or key == glfw.KEY_Q:
                glfw.set_window_should_close(self.win, True)
            if key == glfw.KEY_E:
                self.keys['e'] = True

        if action == glfw.RELEASE:
            if key == glfw.KEY_E:
                self.keys['e'] = False


    def on_mouse_button(self, _win, button, action, _mods):
        if action == glfw.PRESS:
            if button == glfw.MOUSE_BUTTON_LEFT:
                self.clicks["left"] = True
            if button == glfw.MOUSE_BUTTON_RIGHT:
                self.clicks["right"] = True

        if action == glfw.RELEASE:
            if button == glfw.MOUSE_BUTTON_LEFT:
                self.clicks["left"] = False
            if button == glfw.MOUSE_BUTTON_RIGHT:
                self.clicks["right"] = False

    def on_mouse(self, _win, xpos, ypos):
        scroll_sensivity = 0.1

        if xpos < scroll_sensivity*self.width and xpos > 0:
            self.move_x = -self.camera.speed
        elif xpos > (1-scroll_sensivity)*self.width and xpos < self.width:
            self.move_x = self.camera.speed
        else:
            self.move_x = 0

        if ypos < scroll_sensivity*self.height and ypos > 0:
            self.move_y = -self.camera.speed
        elif ypos > (1-scroll_sensivity)*self.height and ypos < self.height:
            self.move_y = self.camera.speed
        else:
            self.move_y = 0

    def on_scroll(self, _win, xoffset, yoffset):
        if yoffset < 0:
            self.camera.position += vec(0, self.camera.zoom_speed*self.delta_time*self.camera.zoom_factor, 0)
            self.camera.position += vec(0, 0, self.camera.zoom_speed*self.delta_time*self.camera.zoom_factor)
        else:
            self.camera.position -= vec(0, self.camera.zoom_speed*self.delta_time*self.camera.zoom_factor, 0)
            self.camera.position -= vec(0, 0, self.camera.zoom_speed*self.delta_time*self.camera.zoom_factor)

    def window_resize(self, _window, _width, _height):
        self.width, self.height = _width, _height
        glViewport(0, 0, _width, _height)
        winsize = glfw.get_window_size(self.win)
        self.projection = self.trackball.projection_matrix(winsize)
        self.mouse_picker.projection_matrix = self.projection



# ========== Main function and initialization =================================
if __name__ == "__main__":
    if not glfw.init():
        exit()
    viewer = Viewer()
    viewer.run()
    glfw.terminate()
