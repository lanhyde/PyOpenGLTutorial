from Engine3.glapp.LoadMesh import LoadMesh
from Engine3.glapp.Utils import create_program
from glapp.pyOGLapp import *
from glapp.Light import *
from glapp.Material import *

class MultiShaders(PyOGLApp):
    def __init__(self):
        super().__init__(pygame.Vector2(850, 200), pygame.Vector2(1000, 800))
        self.light = None
        self.plane = None
        self.cube = None
        glEnable(GL_CULL_FACE)

    def initialize(self):
        mat = Material("shaders/texturevert.glsl", "shaders/texturefrag.glsl")
        self.camera = Camera(self.screenSize.x, self.screenSize.y)
        self.plane = LoadMesh("models/plane.obj", "textures/window.png", GL_TRIANGLES,
                              location=pygame.Vector3(0, 0, 0), material=mat)
        self.cube = LoadMesh("models/cube.obj", "textures/crate.png", GL_TRIANGLES,
                             location=pygame.Vector3(0, -1, 0), material=mat)
        self.light = Light(pygame.Vector3(0, 1, 0), pygame.Vector3(1, 1, 1), 0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def camera_init(self):
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.cube.draw(self.camera, self.light)
        self.plane.draw(self.camera, self.light)


MultiShaders().mainloop()
