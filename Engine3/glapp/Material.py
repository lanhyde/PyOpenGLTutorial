from .Utils import *

class Material:
    def __init__(self, vertexShader, fragmentShader):
        self.program_id = create_program(open(vertexShader).read(), open(fragmentShader).read())

    def use(self):
        glUseProgram(self.program_id)
