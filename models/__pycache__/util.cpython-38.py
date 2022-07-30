# uncompyle6 version 3.7.3
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.5 (tags/v3.8.5:580fbb0, Jul 20 2020, 15:57:54) [MSC v.1924 64 bit (AMD64)]
# Embedded file name: D:\rm2020\3.0\models\util.py
# Compiled at: 2020-08-08 13:12:08
# Size of source mod 2**32: 883 bytes
import math

def clamp(x, minv, maxv):
    return min(maxv, max(minv, x))


def sgn(x, eps=1e-08):
    if abs(x) <= eps:
        return 0
    if x < 0:
        return -1
    return 1


def soft_sgn(x, sharpness=1):
    return math.tanh(sharpness * x)


def normalize_angle(x):
    two_pi = 2 * math.pi
    return math.fmod(math.fmod(x + math.pi, two_pi) + two_pi, two_pi) - math.pi


def log_scale(x, a, b):
    t = (math.exp(x) - 1) / (math.e - 1)
    return a + (b - a) * t
# okay decompiling util.cpython-38.pyc
