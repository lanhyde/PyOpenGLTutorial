import math

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Utils import *
import numpy as np

pygame.init()

screen_width = 800
screen_height = 800
ortho_left = -400
ortho_right = 400
ortho_bottom = 400
ortho_top = -400

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Graphs in PyOpenGL')


def init_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(ortho_left, ortho_right, ortho_top, ortho_bottom)


def plot_point():
    glBegin(GL_POINTS)
    for p in points:
        glVertex2f(p[0], p[1])
    glEnd()


def plot_graph():
    glBegin(GL_LINE_STRIP)
    px: GL_DOUBLE
    py: GL_DOUBLE
    for px in np.arange(0, 4, 0.005):
        py = math.exp(-px) * math.cos(2 * math.pi * px)
        glVertex2f(px, py)
    glEnd()


def plot_lines():
    for l in points:
        glBegin(GL_LINE_STRIP)
        for coords in l:
            glVertex2f(coords[0], coords[1])
        glEnd()


def save_drawing():
    f = open("drawing.txt", "w")
    f.write(str(len(points)) + "\n")
    for l in points:
        f.write(str(len(l)) + "\n")
        for coords in l:
            f.write(str(coords[0]) + " " + str(coords[1]) + "\n")
    f.close()
    print("Drawing Saved")


def load_drawing():
    f = open("drawing.txt", "r")
    num_of_lines = int(f.readline())
    global points
    global lines
    points = []
    lines = []
    for l in range(num_of_lines):
        lines = []
        points.append(lines)
        num_of_coords = int(f.readline())
        for coord_number in range(num_of_coords):
            px, py = [float(value) for value in next(f).split()]
            lines.append((px, py))


def clear_drawing():
    global points
    points.clear()


done = False
init_ortho()
glPointSize(5)

points = []
lines = []

isMouseDown = False
while not done:
    p = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_drawing()
            if event.key == pygame.K_l:
                load_drawing()
            if event.key == pygame.K_SPACE:
                clear_drawing()
        elif event.type == MOUSEBUTTONDOWN:
            isMouseDown = True
            lines = []
            points.append(lines)
        elif event.type == MOUSEMOTION and isMouseDown:
            p = pygame.mouse.get_pos()
            lines.append((map_value(0, screen_width, ortho_left, ortho_right, p[0]),
                         map_value(0, screen_height, ortho_bottom, ortho_top, p[1])))
        elif event.type == MOUSEBUTTONUP:
            isMouseDown = False
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    plot_lines()
    pygame.display.flip()
    # pygame.time.wait(10)
pygame.quit()
