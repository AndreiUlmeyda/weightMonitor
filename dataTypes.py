from typing import TypedDict, Tuple, Optional, NewType

class PixelCoordinate(TypedDict):
    x: int
    y: int

class Calibration(TypedDict):
    northwest: PixelCoordinate
    southwest: PixelCoordinate
    southeast: PixelCoordinate
    northeast: PixelCoordinate

Error = Optional[str]

CalibrationResult = Tuple[Calibration, Error]