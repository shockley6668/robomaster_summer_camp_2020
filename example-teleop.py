#####################################################
# 说明：在“可以修改此处代码”位置书写你的代码
# 
# 尽量不要修改其他地方的代码
#####################################################

from PySide2.QtWidgets import QApplication

from renderer import startRenderer
from simulator import Simulator
from teleop import TeleOp
from models import parameters

import math

class Controller:
    def __init__(self, teleop):
        super().__init__()

        self.teleop = teleop
        ################可以修改此处代码########################
        # 在这里初始化程序变量
        self.odom_x = 0
        self.odom_y = 0
        self.odom_yaw = 0

        self.last_enc = [0 for _ in range(4)]
        ##################结束#################################

    def step(self, dt, sensor_data, set_control_input, submit_prediction):
        #Get encoder data
        encoder = [sensor_data["wheels"][i]["encoder"] for i in range(4)]
        gyro = sensor_data["gyro"]

        ################可以修改此处代码########################
        # 这个函数是控制周期函数，每0.01s会执行一次，你需要在这里书写姿态估计程序
        # 其中 encoder[0..3] 数组为4个编码器读数，单位为rad（注意存在一定误差！）
        # 调用 submit_prediction([x, y]) 提交你估计的机器人中心位置坐标(x, y) 单位为m

        # 这里是简单的累计编码器程序示例，只能计算小车的前进距离，不能转弯平移
        
        #Get encoder deltas
        w=[0, 0, 0, 0]
        for i in range(4):
            if(encoder[i] - self.last_enc[i] > 3.14):
                w[i] = encoder[i] - 2* 3.1415926 - self.last_enc[i]
            elif(encoder[i] - self.last_enc[i] < -3.14):
                w[i] = encoder[i] + 2* 3.1415926 - self.last_enc[i]
            else:
                w[i] = encoder[i] - self.last_enc[i]
        # w = [encoder[i] - self.last_enc[i] for i in range(4)]
        self.last_enc = encoder
        
        #Accumulate

        dx = (w[0] + w[1] + w[2] + w[3]) * parameters.WHEEL_RADIUS / 4
        dy = (-w[0] + w[1] + w[2] - w[3]) * parameters.WHEEL_RADIUS / 4
        self.odom_yaw += (-w[0] + w[1] - w[2] + w[3]) / (
                parameters.CAR_A + parameters.CAR_B) * parameters.WHEEL_RADIUS / 4
        self.odom_x += dx * math.cos(self.odom_yaw) - dy * math.sin(self.odom_yaw)
        self.odom_y += dx * math.sin(self.odom_yaw) + dy * math.cos(self.odom_yaw)
        #Submit
        submit_prediction([0, 0])
        ############################################################

        #get teleop data
        wheel_torque = self.teleop.getControlInput()
        wheel_torque=[0,0,0.5,0]

        #Output control signals
        set_control_input({
            "wheels": [{"torque": wheel_torque[i]} for i in range(4)]
        })

app = QApplication([])
teleop = TeleOp()
controller = Controller(teleop)
simulator = Simulator(controller)

startRenderer(app, simulator)