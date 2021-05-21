# Author: Isaac Chang
# Contact: chang.isaac@outlook.com
# Date: 03/16/2021

import numpy as np

class PoseMath:
    """
    This class contains static functions for calculating the angle between joints
    extracted from OpenPose. It uses the numpy library for vector calculations.
    Currently only supports 2D joint points.
    """

    @staticmethod
    def make_vector(p1, p2):
        """
        Creates and returns a numpy vector (1D array) going from p1 to p2.
        Expects points to be given in the form [x_coord, y_coord].
        """
        x_diff = p2[0] - p1[0]
        y_diff = p2[1] - p1[1]

        return np.array([x_diff, y_diff])

    @staticmethod
    def get_angle_between(v1, v2, in_deg=False):
        """
        Calculates and returns the angle in radians or degrees between 2 vectors.
        Currently only supports 2D joint points.
        """

        unit_v1 = v1 / np.linalg.norm(v1)
        unit_v2 = v2 / np.linalg.norm(v2)
        dot_product = np.dot(unit_v1, unit_v2)
        angle = np.arccos(dot_product)

        if in_deg:
            return np.rad2deg(angle)

        return angle
