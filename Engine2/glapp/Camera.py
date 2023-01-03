import pygame
from OpenGL.GLU import *
from math import *
import numpy as np

from .Transformations import identity_mat, rotate, translate
from .Uniform import Uniform


class Camera:
    def __init__(self, program_id, w, h):
        self.transformation = identity_mat()
        self.last_mouse = pygame.math.Vector2(0, 0)
        self.mouse_sensitivityX = 0.1
        self.mouse_sensitivityY = 0.1
        self.key_sensitivity = 0.008
        self.projection_mat = self.perspective_mat(60, w / h, 0.01, 10000)
        self.projection = Uniform("mat4", self.projection_mat)
        self.projection.find_variable(program_id, "projection_mat")
        self.program_id = program_id
        self.screen_width = w
        self.screen_height = h

    def perspective_mat(self, fov, aspect_ratio, near, far):
        rad = radians(fov)
        d = 1.0 / tan(rad / 2)
        r = aspect_ratio
        b = (far + near) / (near - far)
        c = far * near / (near - far)
        return np.array([[d / r, 0, 0, 0], [0, d, 0, 0], [0, 0, b, c], [0, 0, -1, 0]], np.float32)


    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_change = self.last_mouse - pygame.math.Vector2(mouse_pos)
        pygame.mouse.set_pos(self.screen_width / 2, self.screen_height / 2)
        self.last_mouse = pygame.mouse.get_pos()
        self.rotate(mouse_change.x * self.mouse_sensitivityX, mouse_change.y * self.mouse_sensitivityY)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.transformation = translate(self.transformation, 0, 0, self.key_sensitivity)
        if keys[pygame.K_UP]:
            self.transformation = translate(self.transformation, 0, 0, -self.key_sensitivity)
        if keys[pygame.K_LEFT]:
            self.transformation = translate(self.transformation, -self.key_sensitivity, 0, 0)
        if keys[pygame.K_RIGHT]:
            self.transformation = translate(self.transformation, self.key_sensitivity, 0, 0)

        self.projection.load()
        lookat_mat = self.transformation
        lookat = Uniform("mat4", lookat_mat)
        lookat.find_variable(self.program_id, "view_mat")
        lookat.load()

    def rotate(self, yaw, pitch):
        self.transformation = rotate(self.transformation, yaw, "y")
        self.transformation = rotate(self.transformation, pitch, "x")