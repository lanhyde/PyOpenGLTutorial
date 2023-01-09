#version 330 core

in vec3 color;
in vec3 normal;
in vec3 fragpos;
in vec3 view_pos;
in vec2 uv;
out vec4 frag_color;

struct light {
    vec3 position;
    vec3 color;
};
#define NUM_LIGHTS 3
uniform light light_data[NUM_LIGHTS];
uniform sampler2D tex;

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
    frag_color = frag_color * texture(tex, uv);
}