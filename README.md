# RoboMaster 夏令营嵌入式任务

## 环境安装说明

1. 安装Python 3.8（[官网下载](https://www.python.org/downloads/)或者[Anaconda环境](https://www.anaconda.com/products/individual)）

2. 安装依赖库

```bash
pip install -r requirements.txt 
```
3. 在本目录下打开终端并且运行示例程序
```bash
python example-teleop.py
```

## 模拟器使用说明

### 前言

我们的模拟器模拟RoboMaster EP机器人，使用麦克纳姆轮，可以参照RoboMaster EP技术文档，所有量均为标准单位制(SI)，机器人具体参数可以参考```models/parameters.py```

### 界面说明

模拟器界面中为场地，右下角有方框中显示机器人信息

蓝白色线条为机器人的轨迹，绿色为估计的轨迹

其中 X，Y为坐标，Yaw为朝向角（单位为度）

Vx，Vy，Vw 为速度和角速度

Err 为姿态估计的平均误差

### 调整界面大小

界面被设置为固定大小，启动后无法拉伸。若要改变界面的大小，请在调用startRenderer(app, simulator)时传入长度为2的一个元组给size（分别描述宽和长的像素个数）。

例：
```bash
startRenderer(app, simulator, size = (1280,1720))
```

### 程序交互说明

example.py 为轨迹模式，机器人会跟随特定轨迹运动

example-teleop.py 为遥控模式，你可以操作机器人运动

你的任务是根据机器人上面的传感器读数确定机器人的位置。

你需要参考并且修改 example.py / example-teleop.py，编写机器人位置估计程序。

模拟器每0.01s会调用一次step函数，其中我们提供的encoder数组为编码器读数，gyro为陀螺仪读数，acc为加速度计读书，请在这里编写你的位置估计程序，并且调用submit_prediction函数提交你估计的机器人当前位置。

## 示例

example.py / example-teleop.py 中包含最简单的位置估计程序，只有在机器人走直线不转弯时有效

## 任务

### 第一阶段

了解不同传感器的特性，设计传感器的模型，并根据csv中的数据，整定模型参数。

### 第二阶段

还原EP在这段轨迹的位移，速度，加速度，角度的变化。通过 submit_prediction 的方法返回计算的坐标。

### 第三阶段

通过Controller类中传入的 set_control_input 方法，向机器人传入力矩以控制EP机器人完成 “RoboMaster”轨迹。

## Controller类

每隔0.01s，Controller类的step函数将会调用，其中的sensor_data, set_control_input和submit_prediction是十分重要的参数和函数

### 传感器数据输入 sensor_data

包含传感器得到的数据，与运动的真实数据存在误差。

### 设置机器人四轮的力矩 set_control_input

set_control_input() 需要传入一个长度为4的列表，其中每一个元素代表对对应轮子设置的力矩。

程序提供TrajectoryPlayer()和TeleOp()的方法进行输入。但是在第三阶段的任务中，需要营员自行传入参数

### 提交预测坐标 submit_prediction

submit_prediction() 需要传入一个长度为2的列表，分别代表预测的横坐标x和纵坐标y。在第二阶段的任务中，营员需要根据sensor_data的数据来预测机器人的坐标。
