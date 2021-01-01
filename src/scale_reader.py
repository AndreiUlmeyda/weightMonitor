# pylint: disable=C0103
"""

This module provides the class ScaleReader.
ScaleReader can be used to read numeric values from an image of a seven
segment display.

"""

from datetime import datetime
import json
import os
from PIL import Image  # type: ignore
from src.config_loader import ConfigLoader
from src.ocr import Ocr


class MissingInputImageError(Exception):
    pass


class MissingConfigLoaderError(Exception):
    pass


class ScaleReader:
    """
    The class ScaleReader can be used to read numeric values from an image of a
    seven segment display.

    This operation has 2 prerequisites:
        1. A sufficiently clear and high contrast image of the display.
        2. Calibration data specifying pixel values of the four corners of
            the seven-segment-display-region of the image. This data can relatively easily be
            obtained using the calibration script inside of the project folder
    The code assumes:
        1. That the numbers in the image have a strong red hue compared to the rest of the image
        2. That the image shows 3 digits

    """
    def __init__(self, configLoader: ConfigLoader) -> None:
        """
        The input image is provided through the constructor
        ! Calibration needs to be done using the same image dimensions !
        """
        if configLoader is None:
            raise MissingConfigLoaderError

        self.configLoader = configLoader
        self.transformedImage = None
        self.archiveFolderName = 'archive/'
        self.fileExtension = '.jpg'
        self.resizeFactor = 4

    def readWeight(self, image: Image) -> float:
        if image is None:
            raise MissingInputImageError
        """
        Transform the input image to isolate the display region.
        Filter for red-ish pixels. Create a mask using those.
        Perform OCR on the mask.

        """

        # Transform the image to isolate the region containing the display.
        # The values specifying the four corners of the display are read from
        # a config file and can be generated by executing 'calibration.py'

        config = self.configLoader.getConfig()

        lcdRegion = image.transform(image, Image.QUAD, [
            config['northwest']['x'], config['northwest']['y'],
            config['southwest']['x'], config['southwest']['y'],
            config['southeast']['x'], config['southeast']['y'],
            config['northeast']['x'], config['northeast']['y']
        ], Image.BILINEAR)

        # Reduce image size for performance reasons
        (width, height) = lcdRegion.size

        smallSize = (width // self.resizeFactor, height // self.resizeFactor)
        smallerImage = lcdRegion.resize(smallSize)

        # Try to isolate red pixels. Generate a 1bit image where
        # a value of 1 means 'above a certain ratio of red to other colors' and
        # a value of 0 measns 'below that'
        redMask = Image.new('1', smallSize)

        for x in range(smallSize[0]):
            for y in range(smallSize[1]):

                pixel = smallerImage.getpixel((x, y))
                red = pixel[0]
                green = pixel[1]
                blue = pixel[2]

                redProportion = max(0, (red - (green + blue)))

                if redProportion > 10:
                    redMask.putpixel((x, y), 1)
                else:
                    redMask.putpixel((x, y), 0)

        # Perform OCR on the image
        (readout, _) = Ocr.read(image=redMask)
        readout = str(readout)

        # Assume the point is at the 3rd position of the readout
        weight = readout[2:4] + '.' + readout[4]

        return weight

    def showDebugImages(self) -> None:
        # TODO redo using tkinter
        pass