import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Cube import *
from Engine.Camera import Camera
from loadMesh import *

pygame.init()

# project settings
screen_width = 1000
screen_height = 800
background_color = (0, 0, 0, 1)
drawing_color = (1, 1, 1, 1)

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('OpenGL in Python')

cube = Cube(GL_LINE_LOOP, position=pygame.Vector3(2, 0, 0), rotation=Rotation(45, pygame.Vector3(1, 0, 0)), scale=pygame.Vector3(0.5, 0.5, 0.5))
cube2 = Cube(GL_LINE_LOOP, position=pygame.Vector3(2, 0, 0), rotation=Rotation(45, pygame.Vector3(1, 0, 0)), scale=pygame.Vector3(2, 2, 2))
mesh = LoadMesh("donuts.obj", GL_LINE_LOOP)

camera = Camera()


def initialise():
    glClearColor(background_color[0], background_color[1], background_color[2], background_color[3])
    glColor(drawing_color)

    # projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, (screen_width / screen_height), 0.1, 100.0)


def draw_world_axes():
    glLineWidth(4)
    glBegin(GL_LINES)
    glColor(1, 0, 0)
    glVertex3d(-1000, 0, 0)
    glVertex3d(1000, 0, 0)

    glColor(0, 1, 0)
    glVertex3d(0, -1000, 0)
    glVertex3d(0, 1000, 0)

    glColor(0, 0, 1)
    glVertex3d(0, 0, -1000)
    glVertex3d(0, 0, 1000)
    glEnd()

    sphere = gluNewQuadric()
    glColor(1, 0, 0)
    glPushMatrix()
    glTranslated(1, 0, 0)
    gluSphere(sphere, 0.05, 10, 10)
    glPopMatrix()

    sphere = gluNewQuadric()
    glColor(0, 1, 0)
    glPushMatrix()
    glTranslated(0, 1, 0)
    gluSphere(sphere, 0.05, 10, 10)
    glPopMatrix()

    sphere = gluNewQuadric()
    glColor(0, 0, 1)
    glPushMatrix()
    glTranslated(0, 0, 1)
    gluSphere(sphere, 0.05, 10, 10)
    glPopMatrix()

    glLineWidth(1)
    glColor(1, 1, 1)

def camera_init():
    # modelview
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glViewport(0, 0, screen.get_width(), screen.get_height())
    glEnable(GL_DEPTH_TEST)
    camera.update(screen.get_width(), screen.get_height())


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    camera_init()
    draw_world_axes()
    cube.draw()
    cube2.draw()

done = False
initialise()
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                done = True
    display()
    pygame.display.flip()
    # pygame.time.wait(10)
pygame.quit()
