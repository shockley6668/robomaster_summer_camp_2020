# uncompyle6 version 3.7.3
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.5 (tags/v3.8.5:580fbb0, Jul 20 2020, 15:57:54) [MSC v.1924 64 bit (AMD64)]
# Embedded file name: D:\rm2020\3.0\models\wheel.py
# Compiled at: 2020-08-08 13:52:14
# Size of source mod 2**32: 1748 bytes
from . import util
from . import parameters
from .motor import Motor
import random, numpy as np

class Wheel:

    def __init__(self, radius=parameters.WHEEL_RADIUS, J=0.0003375, max_torque=parameters.MAX_TORQUE, stddev=0.0014, zro=0.007):
        super().__init__()
        self.radius = radius
        self.J = J
        self.motor = Motor()
        self.max_torque = max_torque
        self.w = 0
        self.pos = 0
        self.zro = random.uniform(-zro, zro)
        self.mat = random.uniform(1.01, 1.02)
        self.stddev = stddev
        self.encoder = 0

    def defaultControlInput(self):
        return {'torque': 0}

    def update(self, dt, control_input):
        torque = self.motor.real_torque(util.clamp(control_input['torque'], -1, 1) * self.max_torque, self.w)
        M = torque
        self.w += M / self.J * dt
        self.pos += self.w * dt
        self.pos = util.normalize_angle(self.pos)
        delta = self.w * dt
        output = delta * self.mat + self.zro
        guass = np.random.normal(0, self.stddev)
        self.encoder += output + guass
        self.encoder = util.normalize_angle(self.encoder)

    def readState(self):
        return {'w':self.w, 
         'pos':self.pos, 
         'encoder':self.encoder}

    def readSensors(self):
        return {'encoder': self.encoder}
# okay decompiling wheel.cpython-38.pyc
