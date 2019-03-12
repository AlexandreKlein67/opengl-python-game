import numpy as np

from view.transform import *

from shader import Shader

from object.map.hexagon import Hexagon
# from objects.layout import Layout


class Grid():
    def __init__(self, radius=0, color=(1.0, 0.0, 0.0, 0.5)):
        self.radius = radius
        self.color = color

        self.shader = Shader("res/shaders/grid")


        self.elements = []
        self.generate()

    def generate(self):
        for q in range(-self.radius,self.radius+1):
            r1 = max(-self.radius, -q - self.radius)
            r2 = min(self.radius, -q + self.radius)
            for r in range(r1,r2+1):
                hex_posisiton = (q, r)
                self.elements.append(Hexagon((q, r), self.color))

        print('successfully generated a grid of %i elements.' % len(self.elements))

    def draw(self, view_projection_matrix):
        for e in self.elements:
            e.draw(view_projection_matrix, self.shader)

    def update(self, mouse_hex_round, click):
        for i, e in enumerate(self.elements):
            if e.center[0] == mouse_hex_round[0] and e.center[1] == mouse_hex_round[1]:
                e.hovered = True
                if click:
                    self.select(e)
            else:
                if e.hovered:
                    e.hovered = False

    def get_hex(center):
        for i, e in enumerate(self.elements):
            if e.center[0] == center[0] and e.center[1] == center[1]:
                return e

    def select(self, hex):
        for e in self.elements:
            e.selected = False
        hex.selected = True
