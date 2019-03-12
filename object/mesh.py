import numpy as np
from PIL import Image
from OpenGL.GL import *

from view.transform import identity, translate, scale, rotate

# -----------------------------------------------------------------------------
def load_mesh(model_filename, texture_filename, rgba=False):

    succes = True

    with open(model_filename) as file:
        content = file.read()

    vertices, texture_coords, normals, faces = process_data(content)
    vertex_buffer, texture_buffer, normal_buffer = create_buffers(vertices, texture_coords, normals, faces)
    try:
        mesh = create_model(vertex_buffer, texture_buffer, normal_buffer)
    except Exception as e:
        succes = False
        print("Error while creating a new mesh from a obj file:\n" + str(e))

    try:
        mesh.set_texture(texture_filename, rgba=rgba)
    except Exception as e:
        succes = False
        print("Error while setting a texture to a mesh: " + str(e))


    return mesh if succes else None


def process_data(text):
    vertices, texture_coords, normals, faces = [], [], [], []

    lines = text.split('\n')
    for line in lines:
        if line.startswith("v "):
            line_vertices = line.split()
            vertices.append((line_vertices[1], line_vertices[2], line_vertices[3]))

        if line.startswith("vt "):
            line_tex_coords = line.split()
            texture_coords.append((line_tex_coords[1], line_tex_coords[2]))

        if line.startswith("vn "):
            line_normals = line.split()
            for i in range(1, 4):
                normals.append((line_normals[1], line_normals[2], line_normals[3]))

        if line.startswith("f "):
            line_faces = line.split()
            for i in range(1, 4):
                faces.append(line_faces[i])

    return vertices, texture_coords, normals, faces


def create_buffers(vertices, textures, normals, faces):

    vertex_buffer, normal_buffer, texture_buffer = [], [], []

    for face in faces:
        values = face.split('/')
        vertex_buffer.extend(vertices[int(values[0]) - 1])
        texture_buffer.extend(textures[int(values[1]) - 1])
        normal_buffer.extend(normals[int(values[2]) - 1])

    vertex_buffer = to_numpy_array(vertex_buffer)
    texture_buffer = to_numpy_array(texture_buffer)
    normal_buffer = to_numpy_array(normal_buffer)

    return vertex_buffer, texture_buffer, normal_buffer


def to_numpy_array(array):
    return np.array(array, np.float32)

def create_model(vertex_buffer, texture_buffer, normal_buffer):

    # print(texture_buffer)
    mesh = Mesh(vertex_buffer)
    mesh.add_buffer(texture_buffer, 2, 2)
    mesh.add_buffer(normal_buffer, 3, 3)
    return mesh

# -----------------------------------------------------------------------------
class Mesh:

    def __init__(self, vertices, indices=None, position=(0, 0, 0)):

        self.translation = identity()
        self.scaling = identity()
        self.rotation = identity()

        self.set_position(position)

        self.draw_count = len(vertices)
        self.array_offset = 0

        self._vertex_array = glGenVertexArrays(1)
        self.bind()

        self.buffers = []
        self.add_buffer(vertices, 3, 0)

        self.index_buffers = {}
        if indices is not None:
            self.add_index_buffer("indices", indices)

        self.textures = {}

        glBindVertexArray(0)

    def add_buffer(self, array, n, index):
        self.bind()

        self.buffers += [glGenBuffers(1)]
        glBindBuffer(GL_ARRAY_BUFFER, self.buffers[-1])
        glBufferData(GL_ARRAY_BUFFER, array, GL_STATIC_DRAW)

        glEnableVertexAttribArray(index)
        glVertexAttribPointer(index, n, GL_FLOAT, GL_FALSE, 0, None)

    def add_index_buffer(self, name, indices):
        self.bind()

        self.index_buffers[name] = (glGenBuffers(1), len(indices))
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.index_buffers[name][0])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

    def set_texture(self, filename, name=None, rgba=False):
        self.bind()

        if not name:
            name = "texture"

        image = Image.open(filename)
        if rgba:
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            data = image.convert("RGBA").tobytes()

        else:
            data = np.array(list(image.getdata()), np.uint8)

        self.textures[name] = glGenTextures(1)
        self.bind_texture(name)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        if rgba:
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        else:
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, data)

        glBindTexture(GL_TEXTURE_2D, 0)

    def bind_texture(self, name):
        if name == None:
            element = next(iter(self.textures.values()))
        else:
            element = self.textures[name]
        glBindTexture(GL_TEXTURE_2D, element)

    def set_position(self, x, y=None, z=None):
        if y == None and z == None:
            self.translation = translate(x[0], x[1], x[2])
        else:
            self.translation = translate(x, y, z)

    def translate(self, x, y=None, z=None):
        self.translation = translate(x, y, z)

    def scale(self, x, y=None, z=None):
        self.scaling = scale(x, y, z)

    def rotate(self, axis=(1., 0., 0.), angle=0.0, radians=None):
        self.rotation = rotate(axis, angle, radians)

    def bind(self):
        glBindVertexArray(self._vertex_array)




    def draw(self, projection_view_matrix, shader, index_buffer_name=None, texture_name=None, draw_mod=GL_TRIANGLES):
        self.bind()
        shader.bind()

        if self.textures:
            self.bind_texture(texture_name)

        mvp = projection_view_matrix @ self.translation @ self.rotation @ self.scaling
        shader.set_model_view_projection(mvp)

        if not self.index_buffers:
            glDrawArrays(draw_mod, self.array_offset, self.draw_count)
        else:
            if not index_buffer_name:
                element = next(iter(self.index_buffers.values()))
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element[0])
                glDrawElements(draw_mod, element[1], GL_UNSIGNED_INT, None)
            else:
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.index_buffers[index_buffer_name][0])
                glDrawElements(draw_mod, self.index_buffers[index_buffer_name][1], GL_UNSIGNED_INT, None)

        glBindTexture(GL_TEXTURE_2D, 0)
        glBindVertexArray(0)
