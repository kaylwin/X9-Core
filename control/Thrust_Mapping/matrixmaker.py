import math


class MatrixMaker(object):
    """
    class to be used to generate the appropriate matrix needed for proper thrust mapping
    """

    def __init__(self, location1x, location1y, location1z, location2x, location2y, location2z,
                 location3x, location3y, location3z, location4x, location4y, location4z,
                 location5x, location5y, location5z, location6x, location6y, location6z,
                 location7x, location7y, location7z, location8x, location8y, location8z):
        """initializes some basic variables based on the thrusters locations relative to the center of mass"""
        self.thruster1 = [location1x, location1y, location1z]
        self.thruster2 = [location2x, location2y, location2z]
        self.thruster3 = [location3x, location3y, location3z]
        self.thruster4 = [location4x, location4y, location4z]
        self.thruster5 = [location5x, location5y, location5z]
        self.thruster6 = [location6x, location6y, location6z]
        self.thruster7 = [location7x, location7y, location7z]
        self.thruster8 = [location8x, location8y, location8z]

        # radii are only in the xy-plane because all force generated by thrusters 1-4 is in xy
        self.radius1 = ((self.thruster1[0] ** 2) + (self.thruster1[1] ** 2)) ** 0.5
        self.radius2 = ((self.thruster2[0] ** 2) + (self.thruster2[1] ** 2)) ** 0.5
        self.radius3 = ((self.thruster3[0] ** 2) + (self.thruster3[1] ** 2)) ** 0.5
        self.radius4 = ((self.thruster4[0] ** 2) + (self.thruster4[1] ** 2)) ** 0.5

        # two radii are needed for each of the z-thrusters (1 in xz, 2 in yz)
        self.radius5_1 = ((self.thruster5[0] ** 2) + (self.thruster5[2] ** 2)) ** 0.5
        self.radius5_2 = ((self.thruster5[1] ** 2) + (self.thruster5[2] ** 2)) ** 0.5
        self.radius6_1 = ((self.thruster6[0] ** 2) + (self.thruster6[2] ** 2)) ** 0.5
        self.radius6_2 = ((self.thruster6[1] ** 2) + (self.thruster6[2] ** 2)) ** 0.5
        self.radius7_1 = ((self.thruster7[0] ** 2) + (self.thruster7[2] ** 2)) ** 0.5
        self.radius7_2 = ((self.thruster7[1] ** 2) + (self.thruster7[2] ** 2)) ** 0.5
        self.radius8_1 = ((self.thruster8[0] ** 2) + (self.thruster8[2] ** 2)) ** 0.5
        self.radius8_2 = ((self.thruster8[1] ** 2) + (self.thruster8[2] ** 2)) ** 0.5

        # rot_angles are the sin value that is used to calculate the moment around the z-axis
        self.rot_angle1 = math.sin(math.acos(abs(self.thruster1[0] / self.radius1)) + math.radians(22))
        self.rot_angle2 = math.sin(math.acos(abs(self.thruster2[0] / self.radius2)) + math.radians(22))
        self.rot_angle3 = math.sin(math.acos(abs(self.thruster3[0] / self.radius3)) + math.radians(22))
        self.rot_angle4 = math.sin((math.radians(90) - math.acos(abs(self.thruster4[0] / self.radius4))) + math.radians(22))

        # two rot_angles are needed for each of the z-thrusters(1 in xz, 2 in yz
        self.rot_angle5_1 = 1 / math.cos(math.atan(self.thruster5[2] / self.thruster5[0]))
        self.rot_angle5_2 = 1 / math.cos(math.atan(self.thruster5[2] / self.thruster5[1]))
        self.rot_angle6_1 = 1 / math.cos(math.atan(self.thruster6[2] / self.thruster6[0]))
        self.rot_angle6_2 = 1 / math.cos(math.atan(self.thruster6[2] / self.thruster6[1]))
        self.rot_angle7_1 = 1 / math.cos(math.atan(self.thruster7[2] / self.thruster7[0]))
        self.rot_angle7_2 = 1 / math.cos(math.atan(self.thruster7[2] / self.thruster7[1]))
        self.rot_angle8_1 = 1 / math.cos(math.atan(self.thruster8[2] / self.thruster8[0]))
        self.rot_angle8_2 = 1 / math.cos(math.atan(self.thruster8[2] / self.thruster8[1]))

    # add proportionality constant to allow for different values (need one for left/right and up/down?)
    def generate_matrix(self): #, lrrelation, udrelation):
        """
        Generates the matrix needed for proper thrust mapping
        :return: numpy matrix 6x8
        """
        """
        Explanation


        Definitions:
        R = right thrusters (Thrusters 2 and 4) (value for the first column on thrusters 2 and 4)
        L = left thrusters (Thrusters 1 and 3) (value for the first column on thrusters 1 and 3)
        U = upper thrusters (Thrusters 1 and 2) (value for the second column on thrusters 1 and 2)
        D = lower thrusters (Thruster 3 and 4) (value for the second column on thruster 3 and 4)
        ROT = Rotation component (value for the last column)
        radiusX is the distance of thruster X from the center of mass
        angleX is the angle needed to determine the force perpendicular to radius to find torque for thruster X
        all thrusters are mounted at 22 degree angles from i vector

        Solving for L and R:

            First solve this system of equations (SOE1):
            R * (radius2 * sin(angle2) + radius4 * sin(angle4) - L * (radius1 * sin(angle1) + radius3 * sin(angle3)) = 1
            (2 * R + 2 * L) * cos(22) = 1

            Then solve this system of equations (SOE2):
            R * (radius2 * sin(angle2) + radius4 * sin(angle4) - L * (radius1 * sin(angle1) + radius3 * sin(angle3)) = 0
            (2 * R + 2 * L) * cos(22) = 1

            find the difference between the L and R values of the two systems
            The L and R values from SOE2 are used in the first column of the matrix
            The differences between the values of SOE1 and SOE2 are the values of the last column

        Solving for U and D:

            System of Equations (SOE3):
            D * (radius3 * sin(angle3) + radius4 * sin(angle4) - U * (radius1 * sin(angle1) + radius2 * sin(angle2)) = 1
            (2 * U + 2 * D) * sin(22) = 1

            System of Equations (SOE4):
            D * (radius3 * sin(angle3) + radius4 * sin(angle4) - U * (radius1 * sin(angle1) + radius2 * sin(angle2)) = 0
            (2 * U + 2 * D) * sin(22) = 1

            use the values of U and D in the second column of the matrix
            Again the difference between the values of SOE4 and SOE3 should be equivalent

        Solving ROT:
            The difference between SOE3 and SOE4 values should be equal to the difference of the values in SOE1 and SOE2
            ROT = abs(SOE2.L - SOE1.L) = abs(SOE2.R - SOE1.R) = abs(SOE4.U - SOE3.U) = abs(SOE4.D - SOE3.D)

        The Matrix should look like:
        |    SOE2.L      SOE4.U     0   0   0   -ROT    |
        |    SOE2.R     -SOE4.U     0   0   0    ROT    |
        |   -SOE2.L      SOE4.D     0   0   0    ROT    |
        |   -SOE2.R     -SOE4.D     0   0   0   -ROT    |
        |       0           0       WIP           0     |
        |       0           0                     0     |
        |       0           0                     0     |
        |       0           0                     0     |
        """
        rads = math.radians(22)     # math uses radians so make a constant radian value of 22 (thruster angle)
        # set up the equality
        # right * (radius2*rot_angle2 + radius4*rot_angle4) - left * (radius1*rot_angle1 + radius3*rot_angle3) = (2*right + 2*left) * cos(22)
        right_coe = (self.radius2 * self.rot_angle2 + self.radius4 * self.rot_angle4) - (2 * math.cos(rads)) # multiply both of left halves by relation if needed (shouldnt have to)
        left_coe = (self.radius1 * self.rot_angle1 + self.radius3 * self.rot_angle3) + (2 * math.cos(rads))
        # solve to determine the value of the left thrusters (assume both halves of the equation = 1)
        left_needed = (1 / math.cos(rads)) / ((left_coe / right_coe) * 2 + 2)
        # use the left value to find the right value
        right_needed = (left_coe / right_coe) * left_needed
        # remove the 2 * right and 2 * left and assume rotation is 0
        # i.e. right * (radius2*rot_angle2 + radius4*rot_angle4) - left * (radius1*rot_angle1 + radius3*rot_angle3) = 0
        right_coe += (2 * math.cos(rads))
        left_coe -= (2 * math.cos(rads))
        # right_coe /= lrrelation
        # left_coe /= lrrelation
        # assuming rotation is zero find the relation between left and right then plug the relationship into 2*right + 2 * left = 1/cos22
        left = 1 / math.cos(rads) / ((left_coe / right_coe) * 2 + 2)
        right = (left_coe / right_coe) * left
        # take absolute value will reapply appropriate signs later
        rot1_1 = abs(left_needed - left)    # * lrrelation
        rot1_2 = abs(right_needed - right)  # * lrrelation
        if abs(rot1_1 - rot1_2) < 0.0000000001:
            print "rot1_1 == rot1_2"
        else:
            print "rot1_1 != rot1_2"

        upper_coe = (self.radius1 * self.rot_angle1 + self.radius2 * self.rot_angle2) + (2 * math.sin(rads))
        lower_coe = (self.radius3 * self.rot_angle3 + self.radius4 * self.rot_angle4) - (2 * math.sin(rads))
        upper_needed = (1 / math.sin(rads)) / ((upper_coe / lower_coe) * 2 + 2)
        lower_needed = (upper_coe / lower_coe) * upper_needed
        upper_coe -= (2 * math.sin(rads))
        lower_coe += (2 * math.sin(rads))
        # upper_coe /= udrelation
        # lower_coe /= udrelation
        upper = (1 / math.sin(rads)) / ((upper_coe / lower_coe) * 2 + 2)
        lower = (upper_coe / lower_coe) * upper
        rot2_1 = abs(upper_needed - upper)  # * udrelation
        rot2_2 = abs(lower_needed - lower)  # * udrelation
        if abs(rot2_1 - rot2_2) < 0.0000000001:
            print "rot2_1 == rot2_2"
        else:
            print "rot2_1 != rot2_2"

        # TODO: implementation for the z thrusters
        lower_z_coe = ((self.rot_angle7_1 * self.radius7_1) + (self.rot_angle8_1 * self.radius8_1)) + 2
        upper_z_coe = ((self.rot_angle5_1 * self.radius5_1) + (self.rot_angle6_1 * self.radius6_1)) - 2
        lower_z_needed = 1 / ((lower_z_coe / upper_z_coe) * 2 + 2)
        upper_z_needed = ((lower_z_coe / upper_z_coe) * lower_z_needed)
        lower_z_coe -= 2
        upper_z_coe += 2
        upper_z = 1 / ((lower_z_coe / upper_z_coe) * 2 + 2)
        lower_z = (lower_z_coe / upper_z_coe) * upper_z
        roty1_1 = abs(lower_z_needed - lower_z)
        roty1_2 = abs(upper_z_needed - upper_z)
        if abs(roty1_1 - roty1_2) < 0.0000000001:
            print "roty1_1 == roty1_2"
        else:
            print "roty1_1 != roty1_2"

        if abs(rot1_1 - rot2_1) < 0.0000000001:
            print "rot1_1 == rot2_1"
        else:
            print "rot1_1 != rot2_1"

        right_z_coe = ((self.rot_angle5_2 * self.radius5_2) + (self.rot_angle7_2 * self.radius7_2)) + 2
        left_z_coe = ((self.rot_angle6_2 * self.radius6_2) + (self.rot_angle8_2 * self.radius8_2)) - 2
        right_z_needed = 1 / ((left_z_coe / right_z_coe) * 2 + 2)
        left_z_needed = (left_z_coe / right_z_coe) * right_z_needed
        left_z_coe += 2
        right_z_coe -= 2
        right_z = 1 / ((left_z_coe / right_z_coe) * 2 + 2)
        left_z = (left_z_coe / right_z_coe) * right_z
        rotx1_1 = abs(right_z - right_z_needed)
        rotx1_2 = abs(left_z - left_z_needed)
        if abs(rotx1_1 - rotx1_2) < 0.0000000001:
            print "rotx1_1 == rotx1_2"
        else:
            print "rotx1_1 != rotx1_2"
        print left_z_needed
        print right_z_needed
        print left_z_coe
        print right_z_coe
        print left_z
        print right_z
        print upper_z
        print lower_z

        print "|\t %0.9f\t %0.9f\t 0.000000000\t 0.000000000\t 0.000000000\t-%0.9f\t|" % (left, upper, rot1_1)
        print "|\t %0.9f\t-%0.9f\t 0.000000000\t 0.000000000\t 0.000000000\t %0.9f\t|" % (right, upper, rot1_1)
        print "|\t-%0.9f\t %0.9f\t 0.000000000\t 0.000000000\t 0.000000000\t %0.9f\t|" % (left, lower, rot1_1)
        print "|\t-%0.9f\t-%0.9f\t 0.000000000\t 0.000000000\t 0.000000000\t-%0.9f\t|" % (right, lower, rot1_1)
        print "|\t 0.000000000\t 0.000000000\t %0.9f\t %0.9f\t %0.9f\t 0.000000000\t|" % (upper_z, roty1_1, rotx1_1)
        print "|\t 0.000000000\t 0.000000000\t %0.9f\t-%0.9f\t %0.9f\t 0.000000000\t|" % (upper_z, roty1_1, rotx1_1)
        print "|\t 0.000000000\t 0.000000000\t %0.9f\t %0.9f\t-%0.9f\t 0.000000000\t|" % (lower_z, roty1_1, rotx1_1)
        print "|\t 0.000000000\t 0.000000000\t %0.9f\t-%0.9f\t-%0.9f\t 0.000000000\t|" % (lower_z, roty1_1, rotx1_1)

# this is for testing and will be removed later
maker = MatrixMaker(3, -1.5, 0, 3, 1, 0,
                    -2, -1.5, 0, -2, 1, 0,
                    1.5, -1, 1, 1.5, 0.5, 1,
                    -1, -1, 1, -1, 0.5, 1)
"""desired = [0, 0, 0, 0, 0, 0]
relation1 = 1
relation2 = 1
try:
    relation1 = desired[0] / desired[5]
except ZeroDivisionError:
    relation1 = 1
try:
    relation2 = desired[1] / desired[5]
except ZeroDivisionError:
    relation2 = 1
if desired[0] == 0:
    relation1 = 1
if desired[1] == 0:
    relation2 = 1"""
maker.generate_matrix()  # relation1, relation2)
