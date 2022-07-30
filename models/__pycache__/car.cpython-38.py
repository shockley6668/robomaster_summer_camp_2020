# uncompyle6 version 3.7.3
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.5 (tags/v3.8.5:580fbb0, Jul 20 2020, 15:57:54) [MSC v.1924 64 bit (AMD64)]
# Embedded file name: D:\rm2020\3.0\models\car.py
# Compiled at: 2020-08-08 13:10:13
# Size of source mod 2**32: 2793 bytes
from .wheel import Wheel
from .gyro import Gyro
from .acc import Acc
from . import util
from . import parameters
import math

class Car:

    def __init__(self, l1=parameters.CAR_A, l2=parameters.CAR_B):
        super().__init__()
        self.l1 = l1
        self.l2 = l2
        self.x = 0
        self.y = 0
        self.yaw = 0
        self.vx = 0
        self.vy = 0
        self.vw = 0
        self.wheels = [Wheel() for _ in range(4)]
        self.gyro = Gyro()
        self.acc = Acc()

    def defaultControlInput(self):
        return {'wheels': [self.wheels[i].defaultControlInput() for i in range(4)]}

    def update(self, dt, control_input):
        wheel_control = control_input['wheels']
        for i in range(4):
            self.wheels[i].update(dt, wheel_control[i])

        w = [self.wheels[i].w for i in range(4)]
        r = self.wheels[0].radius
        aplusb = self.l1 + self.l2
        self.vx = r / 4 * (w[0] + w[1] + w[2] + w[3])
        self.vy = r / 4 * (-w[0] + w[1] + w[2] - w[3])
        self.vw = r / 4 / aplusb * (-w[0] + w[1] - w[2] + w[3])
        self.x += dt * (self.vx * math.cos(self.yaw) - self.vy * math.sin(self.yaw))
        self.y += dt * (self.vx * math.sin(self.yaw) + self.vy * math.cos(self.yaw))
        self.yaw += self.vw * dt
        self.yaw = util.normalize_angle(self.yaw)
        self.acc.update([self.vx, self.vy], dt)
        self.gyro.update([0, 0, self.vw], self.acc.readSensors(), dt)

    def readState(self):
        return {'x':self.x, 
         'y':self.y, 
         'yaw':self.yaw, 
         'vx':self.vx, 
         'vy':self.vy, 
         'vw':self.vw, 
         'wheels':[self.wheels[i].readState() for i in range(4)], 
         'gyro':self.gyro.readState(), 
         'acc':self.acc.readState()}

    def setState(self, state):
        self.x = state.x
        self.y = state.y
        self.yaw = state.yaw
        self.vx = state.vx
        self.vy = state.vy
        self.vw = state.vw
        wheel_state = state['wheels']
        for i in range(4):
            self.wheels[i].setState(wheel_state[i])

        self.gyro.setState(state.gyro)
        self.acc.setState(state.acc)

    def readSensors(self):
        return {'wheels':[self.wheels[i].readSensors() for i in range(4)], 
         'gyro':self.gyro.readSensors(), 
         'acc':self.acc.readSensors()}
# okay decompiling car.cpython-38.pyc
