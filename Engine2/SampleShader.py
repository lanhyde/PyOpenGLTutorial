from Engine2.glapp.GraphicsData import GraphicsData
from Engine2.glapp.Square import Square
from Engine2.glapp.Triangle import Triangle
from glapp.pyOGLapp import *
import numpy as np
from glapp.Utils import *

vertex_shader = r'''
#version 330 core

in vec3 position;
in vec3 vertex_color;
uniform vec3 translation;
out vec3 color; 

void main() {
    vec3 pos = position + translation;
    gl_Position = vec4(pos, 1);
    color = vertex_color;
}
'''

fragment_shader = r'''
#version 330 core

in vec3 color;
out vec4 frag_color;

void main() {
    frag_color = vec4(color, 1);
}
'''

class SampleShader(PyOGLApp):
    def __init__(self):
        super().__init__(pygame.Vector2(850, 200), pygame.Vector2(1000, 800))
        self.vao_ref = None
        self.vertex_count = 0
        self.square = None
        self.triangle = None

    def initialize(self):
        self.program_id = create_program(vertex_shader, fragment_shader)
        self.square = Square(self.program_id, pygame.Vector3(-1, 1, 0))
        self.triangle = Triangle(self.program_id, pygame.Vector3(0.5, -0.5, 0))

    def camera_init(self):
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.program_id)
        self.square.draw()
        self.triangle.draw()

SampleShader().mainloop()