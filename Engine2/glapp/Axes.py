from .Mesh import Mesh
from OpenGL.GL import *

class Axes(Mesh):
    def __init__(self, program_id, location):
        vertices = [[-1000, 0, 0], [1000, 0, 0], [0, -1000, 0], [0, 1000, 0], [0, 0, -1000], [0, 0, 1000]]
        colors = [[1, 0, 0], [1, 0, 0], [0, 1, 0], [0, 1, 0], [0, 0, 1], [0, 0, 1]]
        super().__init__(program_id, vertices, colors, GL_LINES, location)