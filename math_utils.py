import math

def lerp(v0, v1, t):
    """
        linear intelporation between two vectors
    """
    return \
        v0[0] + (v1[0] - v0[0]) * t, \
        v0[1] + (v1[1] - v0[1]) * t


def sqr_magnitude(p0, p1):
    """
        returns square of magnitude of vector p0p1
    """
    return math.pow(p0[0] - p1[0], 2) + math.pow(p0[1] - p1[1], 2)


def normalize(v0):
    """
        returns unit vector
    """
    magnitude = math.sqrt(sqr_magnitude((0, 0), v0))
    return v0[0] / magnitude, v0[1] / magnitude


def clamp(v, min_v, max_v):
    """
        returns value between min_v and max_v
    """
    return min(max(v, min_v), max_v)


def quad(a, b, c):
    """
        returns quadratic equation solutions
    """
    sol = None
    if abs(a) < 1e-6:
        if abs(b) < 1e-6:
            sol = (0, 0) if abs(c) < 1e-6 else None
        else:
            sol = (-c/b, -c/b)
    else:
        disc = b*b - 4*a*c
        if disc >= 0:
            disc = math.sqrt(disc)
            a = 2*a
            sol = ((-b-disc)/a, (-b+disc)/a)

    return sol