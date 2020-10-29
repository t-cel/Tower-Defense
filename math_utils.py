import math

"""
    linear intelporation between two vectors
"""
def lerp(v0, v1, t):
    return \
        v0[0] + (v1[0] - v0[0]) * t, \
        v0[1] + (v1[1] - v0[1]) * t


"""
    returns magnitude of vector p0p1
"""
def sqr_magnitude(p0, p1):
    return math.pow(p0[0] - p1[0], 2) + math.pow(p0[1] - p1[1], 2)


"""
    returns unit vector
"""
def normalize(v0):
    magnitude = math.sqrt(sqr_magnitude((0, 0), v0))
    return v0[0] / magnitude, v0[1] / magnitude

"""
    returns value between min_v and max_v
"""
def clamp(v, min_v, max_v):
    return min(max(v, min_v), max_v)