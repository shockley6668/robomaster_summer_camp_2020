from PySide2.QtWidgets import QWidget, QGridLayout, QPushButton
from models import parameters

class TeleOp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.dimension = 3, 5
        self.keys = [
            [None, "↖", "↑", "↗", None],
            ["↶",  "←", None, "→", "↷"],
            [None, "↙", "↓", "↘", None]
        ]

        self.directions = [
            [None, [1, 1, 0], [1, 0, 0], [1, -1, 0], None],
            [[0, 0, 1], [0, 1, 0], None, [0, -1, 0], [0, 0, -1]],
            [None, [-1, 1, 0], [-1, 0, 0], [-1, -1, 0], None]
        ]

        self.cur_direction = [0, 0, 0]

        #create buttons
        layout = QGridLayout()
        for r in range(self.dimension[0]):
            for c in range(self.dimension[1]):
                if self.keys[r][c] is not None:
                    button = QPushButton()
                    button.setText(self.keys[r][c])
                    button.setFixedSize(32, 32)

                    button.pressed.connect(self.buttonPressed)
                    button.released.connect(self.buttonReleased)

                    layout.addWidget(button, r, c, 1, 1)

        self.setLayout(layout)
        self.show()

    def buttonPressed(self):
        text = self.sender().text()

        for r in range(self.dimension[0]):
            for c in range(self.dimension[1]):
                if self.keys[r][c] == text:
                    self.cur_direction = self.directions[r][c]
                    break

    def buttonReleased(self):
        self.cur_direction = [0, 0, 0]

    def getControlInput(self):
        power = 1.0

        #inverse kinematics
        inv_r = 1 / parameters.WHEEL_RADIUS
        aplusb = parameters.CAR_A + parameters.CAR_B

        vx = self.cur_direction[0] * power
        vy = self.cur_direction[1] * power
        vw = self.cur_direction[2] * power

        w = [
            inv_r * (vx - vy - aplusb * vw),
            inv_r * (vx + vy + aplusb * vw),
            inv_r * (vx + vy - aplusb * vw),
            inv_r * (vx - vy + aplusb * vw),
        ]

        #limit w
        w_limit = power

        w_max = max([abs(i) for i in w])
        if w_max > w_limit:
            w_ratio = w_limit / w_max
            w = [w[i] * w_ratio for i in range(4)]

        return w