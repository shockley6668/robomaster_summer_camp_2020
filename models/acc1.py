# uncompyle6 version 3.7.3
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.5 (tags/v3.8.5:580fbb0, Jul 20 2020, 15:57:54) [MSC v.1924 64 bit (AMD64)]
# Embedded file name: e:\01 Organization & Activities\DJI\04 TA\2020_winter_camp_embedded_system\models\acc.py
# Compiled at: 2020-07-30 15:59:17
# Size of source mod 2**32: 1311 bytes
import random, math, numpy as np

class Acc:

    def __init__(self, stddev=0.01, zro_range=0.05):
        self.last_v = np.zeros((2, 1))
        self.mat = np.zeros((3, 3))
        np.fill_diagonal(self.mat, np.insert(np.random.uniform(1.01, 1.02, size=(1,
                                                                                 2)), 2, 1, axis=1))
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

    def update(self, v, dt):
        current_v = np.array([v], dtype=float).T
        acc = (current_v - self.last_v) / dt
        acc = np.insert(acc, 2, 9.8, axis=0)
        self.last_v = current_v
        output = np.dot(self.mat, acc) + self.zro
        assert output.shape == (3, 1)
        guass = np.random.normal(0, (self.stddev), size=(3, 1))
        self.readings = (output + guass).T.tolist()[0]
# okay decompiling acc.pyc
