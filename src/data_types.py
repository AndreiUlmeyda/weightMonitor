# pylint: disable=C0103,R0903,E0611
"""

Definitions of data types used during calibration

An actual CalibrationResult is a tuple of calibration data together
with an optional error string which can be checked by the calling code.
Only when the error is None should the Calibration be treated as valid.

"""

from typing import TypedDict, Tuple, Optional


class PixelCoordinate(TypedDict):
    """ A two-dimensional integer coordinate.  """
    x: int
    y: int


class Calibration(TypedDict):
    """ Four pixel coordinates representing a tetragonal region. """
    northwest: PixelCoordinate
    southwest: PixelCoordinate
    southeast: PixelCoordinate
    northeast: PixelCoordinate


Error = Optional[str]

CalibrationResult = Tuple[Calibration, Error]
