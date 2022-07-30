# uncompyle6 version 3.7.3
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.5 (tags/v3.8.5:580fbb0, Jul 20 2020, 15:57:54) [MSC v.1924 64 bit (AMD64)]
# Embedded file name: D:\rm2020\3.0\models\gyro.py
# Compiled at: 2020-08-08 13:10:38
# Size of source mod 2**32: 1339 bytes
import random, math, numpy as np

class Gyro:

    def __init__(self, stddev=0.07, zro_range=0.35):
        self.mat = np.random.uniform(0.001, 0.002, size=(3, 3))
        np.fill_diagonal(self.mat, np.random.uniform(1.01, 1.02, size=(1, 3)))
        self.zro = np.random.uniform((-zro_range), (+zro_range), size=(3, 1))
        self.stddev = stddev
        self.readings = [
         0, 0, 0]

    def readState(self):
        return {'readings': self.readings}

    def setState(self, state):
        self.readings = state.readings

    def readSensors(self):
        return self.readings

    def update(self, gyro, acc, dt):
        gyro = np.array([gyro], dtype=float).T
        acc = np.array([acc], dtype=float).T
        output = np.dot(self.mat, gyro) + self.zro
        assert output.shape == (3, 1)
        guass = np.random.normal(0, (self.stddev), size=(3, 1))
        self.readings = (output + guass).T.tolist()[0]
# okay decompiling gyro.cpython-38.pyc
