import numpy as np


class MutatorMatrix(object):

    def __init__(self):
        # these are the locations of the thrusters given in X, Y, Z
        self.loc = np.transpose(np.matrix([[11.2148, -4.7524, 0],
                     [11.2148, 4.7524, 0],
                     [-7.631, -4.7524, 0],
                     [-7.631, 4.7524, 0],
                     [6.0419, -5.5709, 5.6384],
                     [6.0419, 5.5709, 5.6384],
                     [-2.485, -5.5709, 5.6384],
                     [-2.485, 5.5709, 5.6384]]))
        self.loc *= .0254
        z = np.sqrt(1-.342*.342)
        # these are the rotation components of each thruster given by putting origin on the thruster
        # the direction is given by drawing a line from the origin to the point (given in x, Y, Z)
        self.rot = np.transpose(np.matrix([[z, 0.342, 0],
                                           [z, -0.342, 0],
                                           [-z, 0.342, 0],
                                           [-z, -0.342, 0],
                                           [0, 0, 1],
                                           [0, 0, 1],
                                           [0, 0, 1],
                                           [0, 0, 1]]))
        # used for some manipulation later
        self.m = None
        self.thrusterStatus = [0, 0, 0, 0, 0, 0, 0, 0]
        self.mutationMatrix = None

    def generateMatrix(self):
        self.m = self.rot
        temp = np.transpose(np.cross(np.transpose(self.rot), np.transpose(self.loc), 1))
        self.m = np.concatenate((self.m, temp))
        self.turnOffThruster()
        matrix = np.linalg.pinv(self.m)
        matrix[:, 4:6] = matrix[:, 4:6] / 10
        self.mutationMatrix = matrix
        return self.mutationMatrix

    def turnOffThruster(self):
        """
        turns of the appropriate thrusters when the matrix is being generated
        :return:
        """
        for i in range(0, 8):
            if self.thrusterStatus[i] == 1:
                self.m[i, :] = 0

    def setThrusterOff(self, thrusterNum):
        self.thrusterStatus[thrusterNum] = 1
        return self.generateMatrix()

    def setThrusterOn(self, thrusterNum):
        self.thrusterStatus[thrusterNum] = 0
        return self.generateMatrix()

matrix = MutatorMatrix()
print matrix.generateMatrix()