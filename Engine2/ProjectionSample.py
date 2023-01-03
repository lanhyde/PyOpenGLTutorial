from Engine2.glapp.GraphicsData import GraphicsData
from Engine2.glapp.Square import Square
from Engine2.glapp.Triangle import Triangle
from glapp.pyOGLapp import *
import numpy as np
from glapp.Utils import *
from glapp.Axes import *

vertex_shader = r'''
#version 330 core

in vec3 position;
in vec3 vertex_color;
uniform mat4 projection_mat;
uniform mat4 model_mat;
uniform mat4 view_mat;

out vec3 color; 

void main() {
    
    gl_Position = projection_mat * inverse(view_mat) * model_mat * vec4(position , 1);
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

class ProjectionSample(PyOGLApp):
    def __init__(self):
        super().__init__(pygame.Vector2(850, 200), pygame.Vector2(1000, 800))
        self.vao_ref = None
        self.vertex_count = 0
        self.square = None
        self.triangle = None
        self.axes = None

    def initialize(self):
        self.program_id = create_program(vertex_shader, fragment_shader)
        self.square = Square(self.program_id, pygame.Vector3(-1, 1, 0))
        self.triangle = Triangle(self.program_id, pygame.Vector3(0.5, -0.5, 0))
        self.camera = Camera(self.program_id, self.screenSize.x, self.screenSize.y)
        self.axes = Axes(self.program_id, pygame.Vector3(0, 0, 0))
        glEnable(GL_DEPTH_TEST)

    def camera_init(self):
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.program_id)
        self.camera.update()
        self.axes.draw()
        self.square.draw()
        self.triangle.draw()

ProjectionSample().mainloop()