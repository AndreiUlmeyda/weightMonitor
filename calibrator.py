# pylint: disable=C0103,R1705
"""

This module provides a class to record calibration data from pixel coordinates
supplied by, for instance, user mouse input.

"""
from dataTypes import PixelCoordinate, Calibration, CalibrationResult

ERROR_NOT_CALIBRATED = "Error: calibration not finished"


class Calibrator:
    """
    Record PixelCoordinates specifying a tetragonal region
    """
    def __init__(self) -> None:
        self.cornerIndex: int = 0

        zeroCoordinate = PixelCoordinate(x=0, y=0)
        self.calibration = Calibration(northwest=zeroCoordinate,
                                       southwest=zeroCoordinate,
                                       southeast=zeroCoordinate,
                                       northeast=zeroCoordinate)

    def isCalibrated(self) -> bool:
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
        inputCoordinate = PixelCoordinate(x=x, y=y)

        if self.cornerIndex == 0:
            self.calibration["northwest"] = inputCoordinate
        elif self.cornerIndex == 1:
            self.calibration["southwest"] = inputCoordinate
        elif self.cornerIndex == 2:
            self.calibration["southeast"] = inputCoordinate
        elif self.cornerIndex == 3:
            self.calibration["northeast"] = inputCoordinate

        self.cornerIndex += 1

    def getCalibration(self) -> CalibrationResult:
        """
        Return calibration data and, depending on the wether
        calibration was successfully completed beforehand, an error
        """
        if self.isCalibrated():
            return (self.calibration, None)
        else:
            return (self.calibration, ERROR_NOT_CALIBRATED)
