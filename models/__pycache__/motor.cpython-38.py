# uncompyle6 version 3.7.3
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.5 (tags/v3.8.5:580fbb0, Jul 20 2020, 15:57:54) [MSC v.1924 64 bit (AMD64)]
# Embedded file name: D:\rm2020\3.0\models\motor.py
# Compiled at: 2020-08-08 13:10:59
# Size of source mod 2**32: 1469 bytes
from . import parameters
from . import util

class Motor:

    def __init__(self, gear_ratio=1, motor_kt=0.0059333, motor_r=0.194, battery_v=24, damping=0.004, dry_friction=0.05, tau_max=parameters.MAX_TORQUE):
        super().__init__()
        self.gear_ratio = gear_ratio
        self.motor_kt = motor_kt
        self.motor_r = motor_r
        self.battery_v = battery_v
        self.damping = damping
        self.dry_friction = dry_friction
        self.tau_max = tau_max

    def real_torque(self, desired, w):
        tau_des_motor = desired / self.gear_ratio
        i_des = tau_des_motor / (self.motor_kt * 1.5)
        bemf = w * self.gear_ratio * self.motor_kt * 2.0
        v_des = i_des * self.motor_r + bemf
        v_actual = util.clamp(v_des, -self.battery_v, self.battery_v)
        tau_act_motor = 1.5 * self.motor_kt * (v_actual - bemf) / self.motor_r
        tau_act = self.gear_ratio * util.clamp(tau_act_motor, -self.tau_max, self.tau_max)
        tau_act -= self.damping * w + self.dry_friction * util.soft_sgn(w)
        return tau_act
# okay decompiling motor.cpython-38.pyc
