from glapp.pyOGLapp import *

class RefactorTest(PyOGLApp):
    def __init__(self):
        super().__init__(screenPos=pygame.Vector2(850, 200), screenSize=pygame.Vector2(800, 600))

    def initialize(self):
        background_color = (0, 0, 0, 0)
        drawing_color = (1, 1, 1, 1)
        glClearColor(background_color[0], background_color[1], background_color[2], background_color[3])
        glColor(drawing_color)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, (self.screenSize.x / self.screenSize.y), 0.1, 1000.0)

    def camera_init(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glViewport(0, 0, int(self.screenSize.x), int(self.screenSize.y))
        glEnable(GL_DEPTH_TEST)
        self.camera.update(self.screenSize.x, self.screenSize.y)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT |GL_DEPTH_BUFFER_BIT)
        self.draw_world_axes()

RefactorTest().mainloop()

