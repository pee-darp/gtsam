import unittest
from math import pi
import numpy as np

from gtsam_py.circlePose3 import circlePose3
from gtsam_py import gtsam


class TestPose3SLAMExample(unittest.TestCase):
    def test_Pose3SLAMExample(self):
        # Create a hexagon of poses
        hexagon = circlePose3(6, 1.0)
        p0 = hexagon.atPose3(0)
        p1 = hexagon.atPose3(1)

        # create a Pose graph with one equality constraint and one measurement
        fg = gtsam.NonlinearFactorGraph()
        fg.add(gtsam.NonlinearEqualityPose3(0, p0))
        delta = p0.between(p1)
        covariance = gtsam.noiseModel.Diagonal.Sigmas(
            np.array(
                [
                    0.05,
                    0.05,
                    0.05,
                    5.0 * pi / 180,
                    5.0 * pi / 180,
                    5.0 * pi / 180,
                ]
            )
        )
        fg.add(gtsam.BetweenFactorPose3(0, 1, delta, covariance))
        fg.add(gtsam.BetweenFactorPose3(1, 2, delta, covariance))
        fg.add(gtsam.BetweenFactorPose3(2, 3, delta, covariance))
        fg.add(gtsam.BetweenFactorPose3(3, 4, delta, covariance))
        fg.add(gtsam.BetweenFactorPose3(4, 5, delta, covariance))
        fg.add(gtsam.BetweenFactorPose3(5, 0, delta, covariance))

        # Create initial config
        initial = gtsam.Values()
        s = 0.10
        initial.insert(0, p0)
        initial.insert(
            1, hexagon.atPose3(1).retract(s * np.random.randn(6, 1))
        )
        initial.insert(
            2, hexagon.atPose3(2).retract(s * np.random.randn(6, 1))
        )
        initial.insert(
            3, hexagon.atPose3(3).retract(s * np.random.randn(6, 1))
        )
        initial.insert(
            4, hexagon.atPose3(4).retract(s * np.random.randn(6, 1))
        )
        initial.insert(
            5, hexagon.atPose3(5).retract(s * np.random.randn(6, 1))
        )

        # optimize
        optimizer = gtsam.LevenbergMarquardtOptimizer(fg, initial)
        result = optimizer.optimizeSafely()

        pose_1 = result.atPose3(1)
        self.assertTrue(pose_1.equals(p1, 1e-4))


if __name__ == "__main__":
    unittest.main()