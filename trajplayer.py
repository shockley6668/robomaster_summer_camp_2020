import json

class TrajectoryPlayer:
    def __init__(self, trajectory_filename):
        super().__init__()

        f = open(trajectory_filename, "r")
        self.json_data = json.load(f)
        f.close()

        self.index = 0
        self.length = len(self.json_data)

    def getControlInput(self):
        if self.index < self.length:
            w = self.json_data[self.index]
        else:
            w = [0, 0, 0, 0]

        self.index += 1
        return w
        