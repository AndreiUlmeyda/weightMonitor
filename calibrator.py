from dataTypes import PixelCoordinate, Calibration, Error, CalibrationResult

ERROR_NOT_CALIBRATED = "Error: calibration not finished"

class Calibrator:

    def __init__(self) -> None:
        self.cornerIndex: int = 0

        zeroCoordinate = PixelCoordinate(x=0, y=0)
        self.calibration = Calibration(
            northwest = zeroCoordinate,
            southwest = zeroCoordinate,
            southeast = zeroCoordinate,
            northeast = zeroCoordinate
        )

    def isCalibrated(self) -> bool:
        return self.cornerIndex > 3

    def reset(self) -> None:
        self.cornerIndex = 0

    def click(self, x: int, y: int) -> None:
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
        if self.isCalibrated():
            return (self.calibration, None)
        else:
            return (self.calibration, ERROR_NOT_CALIBRATED)