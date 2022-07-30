from PySide2.QtWidgets import QApplication, QWidget, QOpenGLWidget, QDesktopWidget, QVBoxLayout, QMainWindow
from PySide2.QtGui import QPainter, Qt, QColor, QPen, QImage
from PySide2.QtCore import QTimer, QPointF, QRectF
import math

from models import util
from models import parameters

class Renderer(QOpenGLWidget):
    def __init__(self, simulator, parent, step_frequency=100, render_frequency=30, speed_factor=1):
        QOpenGLWidget.__init__(self, parent)

        self.simulator = simulator

        self.step_frequency = step_frequency
        self.render_frequency = render_frequency

        self.step_timer = QTimer()
        self.step_timer.setInterval(1000 / self.step_frequency / speed_factor)
        self.step_timer.timeout.connect(self.step)
        self.step_timer.start()

        self.render_timer = QTimer()
        self.render_timer.setInterval(1000 / self.render_frequency)
        self.render_timer.timeout.connect(self.update)
        self.render_timer.start()

    def step(self):
        self.simulator.step(1 / self.step_frequency)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        #get simulator parameters
        state = self.simulator.readState()

        #get canvas size
        width = self.width()
        height = self.height()

        env_w = parameters.ENV_W
        env_h = parameters.ENV_H

        #coordinate transformation function
        ratio_x = width  / env_w
        ratio_y = height / env_h
        offset_x = width / 2
        offset_y = height / 2

        def transform(x, y):
            return x * ratio_x + offset_x, -y * ratio_y + offset_y

        #clear canvas
        painter.fillRect(0, 0, width, height, QColor(4, 9, 38))

        #draw grid
        painter.setPen(QColor(79, 99, 103))
        x = 0
        while x <= env_w / 2:
            painter.drawLine(QPointF(*transform(x, -env_h / 2)), QPointF(*transform(x, env_h / 2)))
            painter.drawLine(QPointF(*transform(-x, -env_h / 2)), QPointF(*transform(-x, env_h / 2)))
            x += parameters.UNIT_LINE
        y = 0
        while y <= env_h / 2:
            painter.drawLine(QPointF(*transform(-env_w / 2, y)), QPointF(*transform(env_w / 2, y)))
            painter.drawLine(QPointF(*transform(-env_w / 2, -y)), QPointF(*transform(env_w / 2, -y)))
            y += parameters.UNIT_LINE

        #draw axis and axis numbers
        painter.setPen(QPen(QColor(125, 29, 63), 2))
        painter.drawLine(QPointF(*transform(0, -env_h / 2)), QPointF(*transform(0, env_h / 2)))
        painter.drawLine(QPointF(*transform(-env_w / 2, 0)), QPointF(*transform(env_w / 2, 0)))

        x = 0
        while x <= env_w / 2:
            px, py = transform(x, 0)
            painter.drawText(px - 10.0, py, "{:.1f}".format(x))
            px, py = transform(-x, 0)
            painter.drawText(px - 10.0, py, "{:.1f}".format(-x))

            x += parameters.UNIT_LINE / 2
        y = parameters.UNIT_LINE / 2
        while y <= env_h / 2:
            px, py = transform(0, y)
            painter.drawText(px - 8.0, py, "{:.1f}".format(y))
            px, py = transform(0, -y)
            painter.drawText(px - 8.0, py, "{:.1f}".format(-y))

            y += parameters.UNIT_LINE / 2

        #transform to car coordinate
        painter.save()
        painter.translate(*transform(state["x"], state["y"]))
        painter.rotate(90 - state["yaw"] / math.pi * 180)

        #draw car
        half_car_w = ratio_x * (parameters.CAR_W / 2)
        half_car_h = ratio_y * (parameters.CAR_L / 2)
        #body
        painter.setPen(QPen(QColor(184, 216, 216), 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(QRectF(-half_car_w, -half_car_h, half_car_w * 2, half_car_h * 2))
        #head
        painter.setPen(QPen(QColor(233, 215, 88), 3))
        painter.drawLine(QPointF( half_car_w,  -half_car_h), QPointF(-half_car_w,  -half_car_h))

        #wheels
        half_wheel_w = ratio_x * parameters.WHEEL_THICKNESS / 2
        half_wheel_h = ratio_y * parameters.WHEEL_RADIUS
        def drawWheel(xc, yc, pos):
            #wheel base
            painter.setPen(QPen(QColor(184, 216, 216), 1))
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(QRectF(xc - half_wheel_w, yc - half_wheel_h, 2 * half_wheel_w, 2 * half_wheel_h))

            #indicator
            indicator_inverse = False
            indicator_pos = pos / math.pi + 0.5
            if indicator_pos >= 1:
                indicator_pos = 2 - indicator_pos
                indicator_inverse = True
            if indicator_pos <= 0:
                indicator_pos = -indicator_pos
                indicator_inverse = True

            y = yc - (-indicator_pos + 0.5) * half_wheel_h * 2

            painter.setPen(QPen(QColor(233, 215, 88) if indicator_inverse else QColor(239, 111, 108), 2))
            painter.drawLine(QPointF(xc - half_wheel_w, y), QPointF(xc + half_wheel_w, y))
        
        center_w = half_car_w
        center_h = half_car_h - half_wheel_h * 1.5
        drawWheel(-center_w - half_wheel_w, -center_h, state["wheels"][0]["pos"])
        drawWheel( center_w + half_wheel_w, -center_h, state["wheels"][1]["pos"])
        drawWheel(-center_w - half_wheel_w,  center_h, state["wheels"][2]["pos"])
        drawWheel( center_w + half_wheel_w,  center_h, state["wheels"][3]["pos"])

        #restore transformations
        painter.restore()

        #collect trajectory
        pos = state["x"], state["y"]
        linear_vel = math.sqrt(state["vx"] ** 2 + state["vy"] ** 2)

        if not hasattr(self, "traj_image"):
            self.traj_image = QImage(width, height, QImage.Format_ARGB32)
            self.last_pos = pos

        #get color by linear velocity
        color = QColor()
        color.setHslF(0.877, 0.28, util.log_scale(min(1, linear_vel / parameters.MAX_SPEED), 0.6, 1))

        traj_painter = QPainter(self.traj_image)
        traj_painter.setPen(QPen(color, 2))
        traj_painter.drawLine(QPointF(*transform(*self.last_pos)), QPointF(*transform(*pos)))

        self.last_pos = pos

        painter.drawImage(0, 0, self.traj_image)

        #draw user predicted trajectory
        pred_pos = self.simulator.getPredPos()

        if not hasattr(self, "traj_pred_image"):
            self.traj_pred_image = QImage(width, height, QImage.Format_ARGB32)
            self.last_pred_pos = pred_pos

        traj_pred_painter = QPainter(self.traj_pred_image)
        traj_pred_painter.setPen(QPen(QColor(12, 202, 74), 2))
        traj_pred_painter.drawLine(QPointF(*transform(*self.last_pred_pos)), QPointF(*transform(*pred_pos)))

        painter.drawImage(0, 0, self.traj_pred_image)

        self.last_pred_pos = pred_pos

        #draw data numbers
        data_rect_w = width * 0.15
        data_rect_h = height * 0.3
        data_rect = QRectF(width - data_rect_w, height - data_rect_h, data_rect_w, data_rect_h)
        painter.fillRect(data_rect, QColor(79, 99, 103, 128))

        painter.setPen(QColor(255, 255, 255))
        painter.drawText(data_rect, """
    X: {:5.2f} m
    Y: {:5.2f} m
    Yaw: {:5.0f} deg

    Vx: {:5.2f} m/s
    Vy: {:5.2f} m/s
    Vw: {:5.0f} deg/s
    
    Err: {:5.3f} m""".format(
        state["x"],
        state["y"],
        state["yaw"] / math.pi * 180,

        state["vx"],
        state["vy"],
        state["vw"] / math.pi * 180,
        
        self.simulator.getPredError()))

        painter.end()
        

def startRenderer(app, simulator, size=(1280, 720)):
    window = QMainWindow()
    # window.resize(1280, 720)
    assert(len(size)==2)
    window.setFixedSize(size[0], size[1])

    renderer = Renderer(simulator, window)
    window.setCentralWidget(renderer)

    #move to center
    center_point = QDesktopWidget().availableGeometry().center()
    rect = window.frameGeometry()
    rect.moveCenter(center_point)
    window.move(rect.topLeft())

    window.show()

    app.exec_()
