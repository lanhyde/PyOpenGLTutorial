import pygame
from pygame.locals import *
from .Camera import *
import os
from OpenGL.GL import *
from OpenGL.GLU import *

class PyOGLApp():
    def __init__(self, screenPos, screenSize):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (screenPos.x, screenPos.y)
        self.screenSize = screenSize
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
        # this line may cause issues on Windows, set it on Mac only
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 32)
        self.screen = pygame.display.set_mode((screenSize.x, screenSize.y), DOUBLEBUF | OPENGL)
        pygame.display.set_caption('OpenGL in Python')
        self.camera = None
        self.program_id = None
        self.clock = pygame.time.Clock()
    def draw_world_axes(self):
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

    def initialize(self):
        pass

    def display(self):
        pass

    def camera_init(self):
        pass

    def mainloop(self):
        done = False
        self.initialize()
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        done = True

            self.camera_init()
            self.display()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
