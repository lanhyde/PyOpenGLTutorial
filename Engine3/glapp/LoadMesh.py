import random
from .Mesh import *
import pygame

from .Utils import format_vertices


class LoadMesh(Mesh):
    def __init__(self, filename, texture_name, draw_type=GL_TRIANGLES, location=pygame.Vector3(0, 0, 0),
                 rotation=Rotation(0, pygame.Vector3(0, 1, 0)),
                 scale=pygame.Vector3(1, 1, 1),
                 move_rotation=Rotation(0, pygame.Vector3(0, 1, 0)),
                 move_translate=pygame.Vector3(0, 0, 0),
                 move_scale=pygame.Vector3(1, 1, 1),
                 material=None):
        coordinates, triangles, uvs, uv_indices, normals, normal_indices = self.load_drawing(filename)
        vertices = format_vertices(coordinates, triangles)
        vertex_normals = format_vertices(normals, normal_indices)
        vertex_uvs = format_vertices(uvs, uv_indices)
        colors = []
        for i in range(len(vertices)):
            colors.append(1)
            colors.append(1)
            colors.append(1)
        super().__init__(vertices, texture_name, vertex_normals, vertex_uvs,  colors, draw_type, location, rotation, scale, move_rotation, move_translate, move_scale, material)

    def load_drawing(self, filename):
        vertices = []
        triangles = []
        normals = []
        normal_indices = []
        uvs = []
        uv_indices = []
        with open(filename) as fp:
            line = fp.readline()
            while line:
                if line[:2] == 'v ':
                    vx, vy, vz = [float(value) for value in line[2:].split()]
                    vertices.append((vx, vy, vz))
                if line[:2] == 'vn':
                    nx, ny, nz = [float(value) for value in line[3:].split()]
                    normals.append((nx, ny, nz))
                if line[:2] == 'vt':
                    tx, ty = [float(value) for value in line[3:].split()]
                    uvs.append((tx, ty))
                if line[:2] == "f ":
                    t1, t2, t3 = [value for value in line[2:].split()]
                    triangles.append([int(value) for value in t1.split('/')][0] - 1)
                    triangles.append([int(value) for value in t2.split('/')][0] - 1)
                    triangles.append([int(value) for value in t3.split('/')][0] - 1)

                    uv_indices.append([int(value) for value in t1.split('/')][1] - 1)
                    uv_indices.append([int(value) for value in t2.split('/')][1] - 1)
                    uv_indices.append([int(value) for value in t3.split('/')][1] - 1)

                    normal_indices.append([int(value) for value in t1.split('/')][2] - 1)
                    normal_indices.append([int(value) for value in t2.split('/')][2] - 1)
                    normal_indices.append([int(value) for value in t3.split('/')][2] - 1)
                line = fp.readline()
        return vertices, triangles, uvs, uv_indices, normals, normal_indices