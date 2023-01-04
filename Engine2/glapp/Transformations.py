import numpy as np
from math import *

class Rotation:
    def __init__(self, angle, axis):
        self.angle = angle
        self.axis = axis

def identity_mat():
    return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)

def translate_mat(x, y, z):
    return np.array([[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]], np.float32)

def scale_mat(s):
    return np.array([[s, 0, 0, 0], [0, s, 0, 0], [0, 0, s, 0], [0, 0, 0, 1]], np.float32)

def scale_mat3(sx, sy, sz):
    return np.array([[sx, 0, 0, 0], [0, sy, 0, 0], [0, 0, sz, 0], [0, 0, 0, 1]], np.float32)

def rotate_x_mat(angle):
   c = cos(radians(angle))
   s = sin(radians(angle))
   return np.array([[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]], np.float32)

def rotate_y_mat(angle):
    c = cos(radians(angle))
    s = sin(radians(angle))
    return np.array([[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]], np.float32)

def rotate_z_mat(angle):
    c = cos(radians(angle))
    s = sin(radians(angle))
    return np.array([[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)

def rotate_axis(angle, axis):
    axis = axis.normalize()
    c = cos(radians(angle))
    s = sin(radians(angle))
    ux = axis.x
    uy = axis.y
    uz = axis.z
    ux2 = ux * ux
    uy2 = uy * uy
    uz2 = uz * uz
    return np.array([[c + ux2 * (1 - c), ux * uy * (1 - c) - uz * s, ux * uz * (1 - c) + uy * s, 0],
                     [uy * ux * (1 - c) + uz * s, c + uy2 * (1 - c), uy * uz * (1 - c) - ux * s, 0],
                     [ux * uz * (1 - c) - uy * s, uz * uy * (1 - c) + ux * s, c + ux2 * (1 - c), 0],
                     [0, 0, 0, 1]], np.float32)

def translate(matrix, x, y, z):
    trans = translate_mat(x, y, z)
    return matrix @ trans

def scale(matrix, s):
    sc = scale_mat(s)
    return matrix @ sc

def scale3(matrix, x, y, z):
    sc = scale_mat3(x, y, z)
    return matrix @ sc

def rotate(matrix, angle, axis, local = True):
    rot = identity_mat()
    if axis.lower() == "x":
        rot = rotate_x_mat(angle)
    elif axis.lower() == "y":
        rot = rotate_y_mat(angle)
    elif axis.lower() == "z":
        rot = rotate_z_mat(angle)
    if local:
        return matrix @ rot
    else:
        return rot @ matrix

def rotateAround(matrix, angle, axis, local = True):
    rot = rotate_axis(angle, axis)
    if local:
        return matrix @ rot
    else:
        return rot @ matrix