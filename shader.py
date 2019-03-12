
from OpenGL.GL import *

def load_shader(shader_file):
    shader_source = ""
    with open(shader_file) as f:
        shader_source = f.read()
    f.close()

    return str.encode(shader_source)


def check_shader_error(shader, flag, is_program, error_message):
    error = []

    if is_program:
        succes = glGetProgramiv(shader, flag)
    else:
        succes = glGetShaderiv(shader, flag)

    if succes == GL_FALSE:
        if is_program:
            error = glGetProgramInfoLog(shader)
        else:
            error = glGetShaderInfoLog(shader)

        print(error_message, ": \"", error, "\"")

def create_shader(text, shader_type):

    shader = glCreateShader(shader_type)

    if shader == 0:
        print("Error: Shader creation failed!")

    glShaderSource(shader, text)
    glCompileShader(shader)

    check_shader_error(shader, GL_COMPILE_STATUS, False, "Error: Shader compilation failed: ")
    return shader


class Shader:

    def __init__(self, filename):

        self._NUM_SHADERS = 2

        self._program = glCreateProgram()

        self._shaders = []
        self._shaders.append(create_shader(load_shader(filename + ".vertex"), GL_VERTEX_SHADER))
        self._shaders.append(create_shader(load_shader(filename + ".fragment"), GL_FRAGMENT_SHADER))

        for i in range(self._NUM_SHADERS):
            glAttachShader(self._program, self._shaders[i])

        glBindAttribLocation(self._program, 0, "position")
        glBindAttribLocation(self._program, 1, "color")
        glBindAttribLocation(self._program, 2, "texture")

        glLinkProgram(self._program)
        check_shader_error(self._program, GL_LINK_STATUS, True, "Error: Program linking failed: ")

        glValidateProgram(self._program)
        check_shader_error(self._program, GL_VALIDATE_STATUS, True, "Error: Program is invalid: ")


    # def __del__(self):
    #     for i in range(self._NUM_SHADERS):
    #         glDetachShader(self._program, self._shaders[i])
    #         glDeleteShader(self._shaders[i])
    #
    #     glDeleteProgram(self._program)

    def bind(self):
        glUseProgram(self._program)

    def set_model_view_projection(self, matrix):
        matrix_location = glGetUniformLocation(self._program, 'u_MVP')
        glUniformMatrix4fv(matrix_location, 1, True, matrix)

    def set_color(self, r, g=None, b=None, a=None):
        color_location = glGetUniformLocation(self._program, 'u_color')

        if not g and not b and not a:
            glUniform4f(color_location, r[0], r[1], r[2], r[3])
        else:
            glUniform4f(color_location, r, g, b, a)
