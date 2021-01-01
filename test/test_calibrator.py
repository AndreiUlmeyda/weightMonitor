# pylint: disable=C0103,C0111
import unittest
from src.calibrator import Calibrator


class TestCalibration(unittest.TestCase):
    def setUp(self) -> None:
        self.calibrator = Calibrator()

    def testUncalibratedWithoutActions(self) -> None:
        (_, error) = self.calibrator.getCalibration()

        self.assertIsNotNone(error)

    def testUncalibratedAfterOneClick(self) -> None:
        self.calibrator.click(x=0, y=0)
        (_, error) = self.calibrator.getCalibration()

        self.assertIsNotNone(error)

    def testCalibratedAfterFourClicks(self) -> None:
        for _ in range(4):
            self.calibrator.click(x=0, y=0)
        (calibration, error) = self.calibrator.getCalibration()

        self.assertIsNone(error)
        self.assertIsNotNone(calibration)

    def testUncalibratedAfterFourClicksAndReset(self) -> None:
        for _ in range(4):
            self.calibrator.click(x=0, y=0)
        self.calibrator.reset()

        (_, error) = self.calibrator.getCalibration()

        self.assertIsNotNone(error)

    def testCalibratedAfterMoreThanFourClicks(self) -> None:
        for _ in range(15):
            self.calibrator.click(x=0, y=0)
        (calibration, error) = self.calibrator.getCalibration()

        self.assertIsNone(error)
        self.assertIsNotNone(calibration)


if __name__ == '__main__':
    unittest.main()
