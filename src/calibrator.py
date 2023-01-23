# pylint: disable=C0103,R1705
"""

This module provides a class to record calibration data from pixel coordinates
supplied by, for instance, user mouse input.

"""
from src.data_types import PixelCoordinate, Calibration, CalibrationResult

ERROR_NOT_CALIBRATED = "Error: calibration not finished"


class Calibrator:
    """
    Record PixelCoordinates specifying a tetragonal region
    """
    def __init__(self) -> None:
        self.cornerIndex: int = 0

        zero_coordinate = PixelCoordinate(x=0, y=0)
        self.calibration = Calibration(northwest=zero_coordinate,
                                       southwest=zero_coordinate,
                                       southeast=zero_coordinate,
                                       northeast=zero_coordinate)

    def is_calibrated(self) -> bool:
        """
        Indicate whether all four corners have been set
        """
        return self.cornerIndex > 3

    def reset(self) -> None:
        """
        Start over at the initial corner
        """
        self.cornerIndex = 0

    def click(self, x: int, y: int) -> None:
        """
        Record successive pixel coordinates counter-clockwise starting
        at the north-west corner of a tetragon
        """
        input_coordinate = PixelCoordinate(x=x, y=y)

        if self.cornerIndex == 0:
            self.calibration["northwest"] = input_coordinate
        elif self.cornerIndex == 1:
            self.calibration["southwest"] = input_coordinate
        elif self.cornerIndex == 2:
            self.calibration["southeast"] = input_coordinate
        elif self.cornerIndex == 3:
            self.calibration["northeast"] = input_coordinate

        self.cornerIndex += 1

    def get_calibration(self) -> CalibrationResult:
        """
        Return calibration data and, depending on the whether
        calibration was successfully completed beforehand, an error
        """
        if self.is_calibrated():
            return self.calibration, None
        else:
            return self.calibration, ERROR_NOT_CALIBRATED
