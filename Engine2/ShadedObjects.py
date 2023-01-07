from Engine2.glapp.LoadMesh import LoadMesh
from glapp.pyOGLapp import *
from glapp.Axes import *
from glapp.Cube import *
from glapp.Light import *

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
out vec3 fragpos;
out vec3 view_pos;

void main() {
    view_pos = vec3(inverse(model_mat) * view_mat[3]);
    gl_Position = projection_mat * inverse(view_mat) * model_mat * vec4(position , 1);
    normal = mat3(transpose(inverse(model_mat))) * vertex_normal;
    fragpos = vec3(model_mat * vec4(position, 1));
    color = vertex_color;
}
'''

fragment_shader = r'''
#version 330 core

in vec3 color;
in vec3 normal;
in vec3 fragpos;
in vec3 view_pos;
out vec4 frag_color;

struct light {
    vec3 position;
    vec3 color;
};
#define NUM_LIGHTS 3
uniform light light_data[NUM_LIGHTS];

vec4 createLight(vec3 light_pos, vec3 light_color, vec3 normal, vec3 fragpos, vec3 view_dir) {
    // ambient
    float strength = 0.1;
    vec3 ambient = light_color * strength;
    // diffuse
    vec3 norm = normalize(normal);
    vec3 light_dir = normalize(light_pos - fragpos);
    float diff = max(dot(norm, light_dir), 0);
    vec3 diffuse = diff * light_color;
    
    // specular
    float specular_strength = 0.8;
    vec3 reflect_dir = reflect(-light_dir, norm);
    float spec = pow(max(dot(view_dir, reflect_dir), 0), 32);
    vec3 specular = spec * light_color * specular_strength;
    return vec4(color * (ambient + diffuse + specular), 1);
}

void main() {
    vec3 view_dir = normalize(view_pos - fragpos);
    for(int i = 0; i < NUM_LIGHTS; i++) {
        frag_color += createLight(light_data[i].position, light_data[i].color, normal, fragpos, view_dir);
    }
}
'''


class ShadedObjects(PyOGLApp):
    def __init__(self):
        super().__init__(pygame.Vector2(850, 200), pygame.Vector2(1000, 800))
        self.light = None
        self.light2 = None
        self.light3 = None
        self.monkey = None
    def initialize(self):
        self.program_id = create_program(vertex_shader, fragment_shader)
        self.camera = Camera(self.program_id, self.screenSize.x, self.screenSize.y)
        self.monkey = LoadMesh("models/suzanne.obj", self.program_id, GL_TRIANGLES, location=pygame.Vector3(0, -1, 2), move_rotation=Rotation(2, pygame.Vector3(1, 1, -1)))
        self.light = Light(self.program_id, pygame.Vector3(2, 1, 2), pygame.Vector3(1, 0, 0), 0)
        self.light2 = Light(self.program_id, pygame.Vector3(-2, 1, -2), pygame.Vector3(0, 1, 0), 1)
        self.light3 = Light(self.program_id, pygame.Vector3(0, 1, 0), pygame.Vector3(0, 0, 1), 2)
        glEnable(GL_DEPTH_TEST)

    def camera_init(self):
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.program_id)
        self.camera.update()
        self.light.update()
        self.light2.update()
        self.light3.update()
        self.monkey.draw()

ShadedObjects().mainloop()
