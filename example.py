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
from trajplayer import TrajectoryPlayer
import numpy as np
import math
import json
import random

################可以修改此处代码########################
# 模式，遥控或者轨迹
MODE = "trajectory"
# MODE = "teleop"

# 在这里输入轨迹文件路径，其中
# trajectories/line.json 为向前走直线
# trajectories/two_lines.json 直走，旋转，向左平移
# trajectories/rm_letter.json 为画 RM 字母
# trajectories/rectangle.json 为画矩形
# trajectories/random_walk.json 为四处走动

TRAJECTORY_FILE = "trajectories/random_walk.json"
##################结束#################################

class Controller:
    def __init__(self, teleop):
        super().__init__()

        self.teleop = teleop
        ################可以修改此处代码########################
        # 在这里初始化程序变量
        #合并
        self.odom_x = 0
        self.odom_y = 0
        self.odom_yaw = 0
        #陀螺仪和加速度计
        self.last_dx1=self.last_dy1=0
        self.yaw1 = 0

        self.Vx=0
        self.Vy = 0


        self.lastdx_predict=0
        self.xpredict_var=0.00975352011479727

        self.lastdy_predict = 0
        self.ypredict_var = 0.00950010291330344

        self.lastyaw_predict=0
        self.yawpredict_var=0.06879591708524443

        #编码器

        self.odom_yaw2 = 0
        self.odom_x2 = 0
        self.odom_y2 = 0
        self.last_enc = [0 for _ in range(4)]
        #力矩调试
        self.xiout=0
        self.set=Controller.RoboMaster_set(self)
        self.i=0
        self.yiout = 0
        self.xlast_error=0
        self.ylast_error=0
        ##################结束#################################
        pass

    def RoboMaster_set(self):
        t = 0
        set = []
        y = 0
        x = 0

        def circule(a, b, x, r):
            if abs(x - a) < r:
                y = b + (r ** 2 - (x - a) ** 2) ** 0.5
            else:
                y = b
            return y

        while t < 4:
            t += 0.01
            x -= 0.005
            set.append([x, 0])
        t = round(t, 2)
        while t < 6 and t >= 4:
            t = t + 0.01
            y += 0.005
            set.append([x, y])

        t = round(t, 2)
        while t < 6.5 and t >= 6:
            x = x + 0.003
            t = t + 0.01

            set.append([x, y])

        t = round(t, 2)
        while t < 7.5 and t >= 6.5:
            x = x + 0.0025
            t = t + 0.01
            y = circule(-1.85, 0.75, x, 0.25)
            set.append([x, y])

        t = round(t, 2)
        while t >= 7.5 and round(t, 2) < 9.5:
            x = x - 0.00125
            t += 0.01
            y = -circule(-1.85, 0.75, x, 0.25) + 1.5
            set.append([x, y])
        t = round(t, 2)
        while t < 10 and t >= 9.5:
            x = x - 0.003
            t = t + 0.01

            set.append([x, y])
        while t >= 10 and round(t, 2) < 11:
            x += 0.004
            y -= 0.005
            t += 0.01
            set.append([x, y])
        t = round(t, 2)

        while t >= 11 and round(t, 2) < 12:
            x += 0.0036
            t += 0.01

            set.append([x, y])

        t = round(t, 2)

        while t >= 12 and round(t, 2) < 13:
            t = round(t, 2)
            x += 0.0021
            y = -circule(-1.25, 0.21, x, 0.21) + 0.42
            t += 0.01
            set.append([x, y])

        t = round(t, 2)

        while t >= 13 and round(t, 2) < 15:
            x -= 0.0021
            y = circule(-1.25, 0.21, x, 0.21)
            t += 0.01

            set.append([x, y])
        t = round(t, 2)

        while t >= 15 and round(t, 2) < 16:
            x += 0.0021
            y = -circule(-1.25, 0.21, x, 0.21) + 0.42
            t += 0.01
            set.append([x, y])
        t = round(t, 2)

        while t >= 16 and round(t, 2) < 17:
            x += 0.0025
            t += 0.01
            set.append([x, y])
        t = round(t, 2)
        while t >= 17 and round(t, 2) < 18:
            y += 0.01
            t += 0.01
            set.append([x, y])
        t = round(t, 2)
        while t >= 18 and round(t, 2) < 19:
            y -= 0.005
            t += 0.01
            set.append([x, y])
        t = round(t, 2)

        while t >= 19 and round(t, 2) < 19.5:
            x += 0.003
            set.append([x, y])

            t += 0.01
        t = round(t, 2)

        while t >= 19.5 and round(t, 2) < 20.5:
            x += 0.0025
            y = circule(-0.85, 0.25, x, 0.25)
            t += 0.01
            set.append([x, y])
        t = round(t, 2)

        while t >= 20.5 and round(t, 2) < 21.5:
            t = round(t, 2)
            x -= 0.0025
            y = -circule(-0.85, 0.25, x, 0.25) + 0.5

            t += 0.01
            set.append([x, y])

        while t >= 21.5 and round(t, 2) < 22:
            x -= 0.003
            set.append([x, y])

            t += 0.01
        t = round(t, 2)
        while t >= 22 and round(t, 2) < 24:
            x += 0.00375
            set.append([x, y])

            t += 0.01
        t = round(t, 2)
        # 圆圈
        while t >= 24 and round(t, 2) < 25:
            t = round(t, 2)
            x += 0.0021
            y = -circule(-0.25, 0.21, x, 0.21) + 0.42
            t += 0.01
            set.append([x, y])
        t = round(t, 2)
        while t >= 25 and round(t, 2) < 27:
            x -= 0.0021
            y = circule(-0.25, 0.21, x, 0.21)
            t += 0.01
            set.append([x, y])
        t = round(t, 2)
        while t >= 27 and round(t, 2) < 28:
            t = round(t, 2)
            x += 0.0021
            y = -circule(-0.25, 0.21, x, 0.21) + 0.42
            t += 0.01
            set.append([x, y])
        t = round(t, 2)
        while t >= 28 and round(t, 2) < 28.5:
            x += 0.005
            set.append([x, y])

            t += 0.01
        t = round(t, 2)
        while t >= 28.5 and round(t, 2) < 30.1:
            y += 0.00625
            set.append([x, y])

            t += 0.01
        while t >= 30.1 and round(t, 2) < 31.1:
            y -= 0.005
            x += 0.0025
            set.append([x, y])

            t += 0.01
        t = round(t, 2)
        while t >= 31.1 and round(t, 2) < 32.1:
            y += 0.005
            x += 0.0025
            set.append([x, y])

            t += 0.01
        t = round(t, 2)
        while t >= 32.1 and round(t, 2) < 33.7:
            y -= 0.00625
            set.append([x, y])
            t = round(t, 2)
            t += 0.01

        t = round(t, 2)

        while t >= 33.7 and round(t, 2) < 34.5:
            x += 0.003125
            set.append([x, y])

            t += 0.01
            t = round(t, 2)

        t = round(t, 2)
        while t >= 34.5 and round(t, 2) < 35.5:
            t = round(t, 2)
            x += 0.0020
            y = -circule(0.75, 0.21, x, 0.21) + 0.42
            t += 0.01
            set.append([x, y])
        t = round(t, 2)

        while t >= 35.5 and round(t, 2) < 36.5:
            y += 0.0032
            t += 0.01
            set.append([x, y])
        t = round(t, 2)

        while t >= 36.5 and round(t, 2) < 38.5:
            x -= 0.0018
            y = circule(0.76, 0.46367, x, 0.19)
            t += 0.01
            set.append([x, y])
        t = round(t, 2)

        while t >= 38.5 and round(t, 2) < 40.5:
            x += 0.0018
            y = circule(0.76, 0.46367, x, 0.19)
            t += 0.01
            set.append([x, y])
        t = round(t, 2)

        while t >= 40.5 and round(t, 2) < 41:
            y -= 0.0031
            t += 0.01
            set.append([x, y])
        t = round(t, 2)

        while t >= 41 and round(t, 2) < 41.5:
            x -= 0.004
            t += 0.01
            set.append([x, y])
        t = round(t, 2)

        while t >= 41.5 and round(t, 2) < 42.5:
            x -= 0.0015
            y = circule(0.74, 0.15, x, 0.15)
            t += 0.01
            set.append([x, y])
        t = round(t, 2)
        while t >= 42.5 and round(t, 2) < 43.5:
            x += 0.0015
            y = -circule(0.74, 0.15, x, 0.15) + 0.3
            t += 0.01
            set.append([x, y])
        t = round(t, 2)

        # s
        while t >= 43.5 and round(t, 2) < 44.5:
            x += 0.005
            t += 0.01
            set.append([x, y])
        t = round(t, 2)

        while t >= 44.5 and round(t, 2) < 45.5:
            x += 0.0015
            y = -circule(1.25, 0.15, x, 0.15) + 0.3
            t += 0.01
            set.append([x, y])
        t = round(t, 2)
        while t >= 45.5 and round(t, 2) < 46.5:
            x -= 0.0015
            y = circule(1.25, 0.15, x, 0.15)
            t += 0.01
            set.append([x, y])
        t = round(t, 2)
        while t >= 46.5 and round(t, 2) < 47:
            x -= 0.002
            t += 0.01
            set.append([x, y])
        t = round(t, 2)

        while t >= 47 and round(t, 2) < 48:
            x -= 0.0015
            y = -circule(1.15, 0.45, x, 0.15) + 0.9
            t += 0.01
            set.append([x, y])

        t = round(t, 2)
        while t >= 48 and round(t, 2) < 49:
            x += 0.0015
            y = circule(1.15, 0.45, x, 0.15)
            t += 0.01
            set.append([x, y])
        t = round(t, 2)
        # t
        while t >= 49 and round(t, 2) < 51:
            x += 0.0045

            t += 0.01
            set.append([x, y])
        t = round(t, 2)
        while t >= 51 and round(t, 2) < 51.5:
            x -= 0.005

            t += 0.01
            set.append([x, y])
        t = round(t, 2)
        while t >= 51.5 and round(t, 2) < 52:
            y += 0.003

            t += 0.01
            set.append([x, y])
        t = round(t, 2)
        while t >= 52 and round(t, 2) < 53.5:
            y -= 0.004

            t += 0.01
            set.append([x, y])
        t = round(t, 2)

        while t >= 53.5 and round(t, 2) < 54.5:
            x += 0.0015
            y = -circule(1.95, 0.15, x, 0.15) + 0.3
            t += 0.01
            set.append([x, y])
        t = round(t, 2)

        # e
        while t >= 54.5 and round(t, 2) < 55:
            x += 0.006

            t += 0.01
            set.append([x, y])
        t = round(t, 2)

        while t >= 55 and round(t, 2) < 56:
            x -= 0.0025
            y = -circule(2.25, 0.25, x, 0.25) + 0.5
            t += 0.01
            set.append([x, y])
        t = round(t, 2)

        while t >= 56 and round(t, 2) < 60:
            x += 0.00125
            y = circule(2.25, 0.25, x, 0.25)
            t += 0.01
            set.append([x, y])
        t = round(t, 2)
        while t >= 60 and round(t, 2) < 62:
            x -= 0.0025

            t += 0.01
            set.append([x, y])

        t = round(t, 2)

        while t >= 62 and round(t, 2) < 64:
            x += 0.0014
            y = -circule(2.25, 0.25, x, 0.25) + 0.5
            t += 0.01
            set.append([x, y])
        t = round(t, 2)
        # r
        while t >= 64 and round(t, 2) < 65:
            x += 0.0032

            t += 0.01
            set.append([x, y])
        t = round(t, 2)
        while t >= 65 and round(t, 2) < 66:
            y += 0.003

            t += 0.01
            set.append([x, y])
        t = round(t, 2)

        while t >= 66 and round(t, 2) < 68:
            x += 0.0025
            y = circule(2.85, 0.3, x, 0.25)

            t += 0.01
            set.append([x, y])
        return set

    def X_PID(self,kpi,Ref,Set,max_out,max_imax): #X轴 pid函数
        error = Set - Ref
        pout = kpi[0]*error
        self.xiout += kpi[1]*error
        if self.xiout>=max_imax:
            self.xiout = max_imax
        if self.xiout<=-max_imax:
            self.xiout = -max_imax
        Dout = kpi[2] * (error - self.xlast_error)
        pidout = pout + self.xiout+Dout
        if pidout>=max_out:
            pidout = max_out
        if pidout<=-max_out:
            pidout = -max_out
        self.xlast_error=error
        return pidout

    def Y_PID(self,kpi,Ref,Set,max_out,max_imax): #Y轴 pid函数

        error = Set - Ref
        pout = kpi[0]*error
        self.yiout += kpi[1]*error
        if self.yiout>=max_imax:
            self.yiout = max_imax
        if self.yiout<=-max_imax:
            self.yiout = -max_imax
        Dout = kpi[2] * (error - self.ylast_error)
        pidout = pout + self.yiout+Dout
        if pidout>=max_out:
            pidout = max_out
        if pidout<=-max_out:
            pidout = -max_out
        self.ylast_error=error
        return pidout
    def circule(self,a,b,x,r):
        if abs(x-a)<r:
            y=b+(r**2-(x-a)**2)**0.5
        else:
            y=b
        return y
    def step(self, dt, sensor_data, set_control_input, submit_prediction):
        #Get encoder data
        encoder = [sensor_data["wheels"][i]["encoder"] for i in range(4)]
        gyro = sensor_data["gyro"]
        acc = sensor_data["acc"]



        ################可以修改此处代码########################
        # 这个函数是控制周期函数，每0.01s会执行一次，你需要在这里书写姿态估计程序
        # 其中 encoder[0..3] 数组为4个编码器读数，单位为rad（注意存在一定误差！）
        # 调用 submit_prediction([x, y]) 提交你估计的机器人中心位置坐标(x, y) 单位为m

        # 这里是简单的累计编码器程序示例，只能计算小车的前进距离，不能转弯平移

        #Get encoder deltas
        w=[0, 0, 0, 0]
        #陀螺仪
        yaw1=(gyro[2]+0.300480158903466)*0.98641682*0.01
        Ax=(acc[0]-0.031574933)*0.98941694+0.0305688385621904-random.uniform(-0.01,0.01)
        Ay=(acc[1]-0.027907728)*0.98990419+0.0274278939135515+random.uniform(-0.01,0.01)

        if abs(Ax)<0.09 :
            Ax=0
        if abs(Ay)<0.09 :
            Ay = 0
        # dx1=Ax*0.0001+self.last_dx1
        # dy1=Ay*0.0001+self.last_dy1

        # self.last_dx1 = dx1
        # self.last_dy1 = dy1
        # self.odom_x1+= dx1 * math.cos(self.yaw1) - dy1 * math.sin(self.yaw1)
        # self.odom_y1+= dx1 * math.sin(self.yaw1) + dy1 * math.cos(self.yaw1)




        for i in range(4):
            if(encoder[i] - self.last_enc[i] > 3.14):
                w[i] = encoder[i] - 2* 3.1415926 - self.last_enc[i]
            elif(encoder[i] - self.last_enc[i] < -3.14):
                w[i] = encoder[i] + 2* 3.1415926 - self.last_enc[i]
            else:
                w[i] = encoder[i] - self.last_enc[i]

        # w = [encoder[i] - self.last_enc[i] for i in range(4)]
        self.last_enc = encoder
        #测量值
        w[0] = 0.98284149 * (w[0] - 0.004791132)
        w[1] = 0.98708168 * (w[1] + 0.001241251)
        w[2] = 0.98601081 * (w[2] - 0.000180762)
        w[3] = 0.98734884 * (w[3] - 0.004075892)
        #初试的估计dx就直接用编码器测量的

        #x方向
        xa_std=0.009764070166680645
        xodo_var=0.0000334835943391
        dx= (w[0] + w[1] + w[2] + w[3]) * parameters.WHEEL_RADIUS / 4
        k1=self.xpredict_var/(self.xpredict_var+xodo_var)
        dx_predict=self.lastdx_predict+Ax*0.0001
        self.xpredict_var+=xa_std
        
        dx_predict=dx_predict*(1-k1)+dx*k1

        # self.xpredict_var=(self.xpredict_var*xodo_var)/(self.xpredict_var+xodo_var)
        self.xpredict_var=(1-k1)*self.xpredict_var
        self.lastdx_predict=dx_predict

        #y
        ya_std =0.009764070166680645  #加速度计标准差
        yodo_var = 0.000035110904485 #编码器方差
        dy = (-w[0] + w[1] + w[2] - w[3]) * parameters.WHEEL_RADIUS / 4
        dy_predict = self.lastdy_predict + Ay*0.0001
        # print(dy,dy_predict)
        self.ypredict_var += ya_std
        k2=self.ypredict_var / (self.ypredict_var + yodo_var)

        dy_predict = dy_predict * (1-k2) + dy *k2
        # self.ypredict_var = (self.ypredict_var * yodo_var) / (self.ypredict_var + yodo_var)
        self.ypredict_var=(1-k2)*self.ypredict_var
        self.lastdy_predict = dy_predict


        #Accumulate
        #self.odom_x += (w[0] + w[1] + w[2] + w[3]) * parameters.WHEEL_RADIUS / 4
        # dx = (a + b + c + d) * parameters.WHEEL_RADIUS / 4
        # dy = (-a + b + c - d) * parameters.WHEEL_RADIUS / 4

        yaw_std=0.06879591708524443  #陀螺仪的标准差
        yawodo_var=0.01726640217716041#编码器标准差
        self.yawpredict_var += yaw_std
        yaw_predict = self.lastyaw_predict + yaw1
        k3 = self.yawpredict_var / (self.yawpredict_var + yawodo_var)
        if abs(yaw1)>0.01:
            k3=0.5
        self.odom_yaw+= (-w[0] + w[1] - w[2] + w[3]) / (parameters.CAR_A + parameters.CAR_B) * parameters.WHEEL_RADIUS / 4

        yaw_predict =yaw_predict * (1-k3) + self.odom_yaw *k3
        self.yawpredict_var = (1 - k3) * self.ypredict_var

        self.lastyaw_predict= yaw_predict
        self.odom_x += dx_predict * math.cos(yaw_predict) - dy_predict * math.sin(yaw_predict)
        self.odom_y += dx_predict * math.sin(yaw_predict) + dy_predict * math.cos(yaw_predict)

        #Submit

        submit_prediction([self.odom_x, self.odom_y])

        ##################结束#################################
        # 第一项任务和第二项任务无需修改以下代码
        # 仅在第三项任务中需要修改下面的代码

        #get teleop data
        wheel_torque = self.teleop.getControlInput()
        power = 1

        # inverse kinematics
        inv_r = 1 / parameters.WHEEL_RADIUS
        aplusb = parameters.CAR_A + parameters.CAR_B
        vw=0

        try:
            x_set=self.set[self.i][0]
            y_set = self.set[self.i][1]
        except IndexError:
            x_set=3.0992500000000773
            y_set=0.3193503875920224
        self.i+=1


        vx_set = Controller.X_PID(self, [1.2,0,10], self.odom_x, x_set, 2,0.1)
        vy_set = Controller.Y_PID(self, [1.2, 0,10], self.odom_y, y_set, 2, 0.1)

        w = [
            inv_r * (vx_set - vy_set - aplusb * vw),
            inv_r * (vx_set + vy_set + aplusb * vw),
            inv_r * (vx_set + vy_set - aplusb * vw),
            inv_r * (vx_set - vy_set + aplusb * vw),
        ]
        w_limit = power

        w_max = max([abs(i) for i in w])
        if w_max > w_limit:
            w_ratio = w_limit / w_max
            w = [w[i] * w_ratio for i in range(4)]


        #Output control signals
        set_control_input({ "wheels": [{"torque":  w[i]} for i in range(4)]})  #把w改成wheel_torque可看随机漫步的效果
        

        ##################结束#################################

app = QApplication([])
player = TrajectoryPlayer(TRAJECTORY_FILE) if MODE == "trajectory" else TeleOp()
controller = Controller(player)
simulator = Simulator(controller)
startRenderer(app, simulator, size = (1280, 720)) #可传入size参数调整GUI的大小
