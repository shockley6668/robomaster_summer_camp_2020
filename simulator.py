from models.car import Car
import math
import random
import numpy as np

class Simulator:
    def __init__(self, controller, random_seed=0):
        super().__init__()

        random.seed(random_seed)
        np.random.seed(random_seed)

        self.controller = controller

        self.car = Car()
        self.control_input = self.car.defaultControlInput()

        self.pred_pos = 0.0, 0.0
        self.pred_error = 0
        self.pred_num = 0

    def readState(self):
        return self.car.readState()

    def setControlInput(self, control_input):
        self.control_input.update(control_input)

    def step(self, dt):
        self.controller.step(dt, self.car.readSensors(), self.setControlInput, self.submitPredPos)
        self.car.update(dt, self.control_input)

    def getPredPos(self):
        return self.pred_pos

    def submitPredPos(self, pred_pos):
        self.pred_pos = pred_pos

        #calculate pred error
        state = self.readState()
        pos = [state["x"], state["y"]]

        #pred error avg to move length
        weight = math.sqrt(state["vx"] ** 2 + state["vy"] ** 2)

        self.pred_num += weight
        self.pred_error += weight * ((pred_pos[0] - pos[0]) ** 2 + (pred_pos[1] - pos[1]) ** 2)

    def getPredError(self):
        return math.sqrt(self.pred_error / self.pred_num) if self.pred_num > 0 else 0
