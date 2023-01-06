from Engine2.glapp.LoadMesh import LoadMesh
from glapp.pyOGLapp import *
from glapp.Axes import *
from glapp.Cube import *

vertex_shader = r'''
#version 330 core

in vec3 position;
in vec3 vertex_color;
in vec3 vertex_normal;
uniform mat4 projection_mat;
uniform mat4 model_mat;
uniform mat4 view_mat;

out vec3 color; 
out vec3 normal;
out vec3 fragppos;
out vec3 light_pos;
void main() {
    light_pos = vec3(5, 5, 5);
    gl_Position = projection_mat * inverse(view_mat) * model_mat * vec4(position , 1);
    normal = vertex_normal;
    fragpos = vec3(model_mat * vec4(position, 1));
    color = vertex_color;
}
'''

fragment_shader = r'''
#version 330 core

in vec3 color;
in vec3 normal;
in vec3 fragpos;
in vec3 light_pos;
out vec4 frag_color;

void main() {
    vec3 light_color = vec3(1, 1, 1);
    vec3 norm = normalize(normal);
    vec3 light_dir = normalize(light_pos - fragpos);
    float diff = max(dot(norm, light_dir), 0);
    vec3 diffuse = diff * light_color;
    frag_color = vec4(color * diffuse, 1);
}
'''


class ShadedObjects(PyOGLApp):
    def __init__(self):
        super().__init__(pygame.Vector2(850, 200), pygame.Vector2(1000, 800))
        self.vao_ref = None
        self.vertex_count = 0
        self.axes = None
        self.moving_cube = None
        self.monkey = None
    def initialize(self):
        self.program_id = create_program(vertex_shader, fragment_shader)
        self.camera = Camera(self.program_id, self.screenSize.x, self.screenSize.y)
        # self.axes = Axes(self.program_id, pygame.Vector3(0, 0, 0))
        # self.moving_cube = Cube(self.program_id, location=pygame.Vector3(2, 1, 2), move_rotation=Rotation(1, pygame.Vector3(0, 1, 0)))
        self.monkey = LoadMesh("models/suzanne.obj", self.program_id, GL_TRIANGLES, pygame.Vector3(-2, 1, 2), move_rotation=Rotation(2, pygame.Vector3(1, 1, -1)))
        glEnable(GL_DEPTH_TEST)

    def camera_init(self):
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.program_id)
        self.camera.update()
        # self.axes.draw()
        # self.moving_cube.draw()
        self.monkey.draw()

ShadedObjects().mainloop()
