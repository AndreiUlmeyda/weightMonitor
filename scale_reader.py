# pylint: disable=C0103
"""

This module provides the class ScaleReader.
ScaleReader can be used to read numeric values from an image of a seven
segment display.

"""

from datetime import datetime
import json
import os
import subprocess
from PIL import Image # type: ignore


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
    transformedImage = None
    redMaskImage = None
    archiveFolderName = 'archive/'
    fileExtension = '.jpg'
    timestamp = None

    def __init__(self, image: Image) -> None:
        """
        The input image is provided through the constructor
        ! Calibration needs to be done using the same image dimensions !
        """
        self.inputImage = image
        self.weight = 0

    def readWeight(self) -> float:
        """
        Transform the input image to isolate the display region.
        Filter for red-ish pixels. Create a mask using those.
        Perform OCR on the mask.

        """
        self.timestamp = datetime.now().strftime("%Y%m%d%I%M")

        # transform to try and restore horizontal and vertical lines
        with open('config.json') as file:
            config = json.load(file)

        nw = (config['northwest']['x'], config['northwest']['y'])
        sw = (config['southwest']['x'], config['southwest']['y'])
        se = (config['southeast']['x'], config['southeast']['y'])
        ne = (config['northeast']['x'], config['northeast']['y'])

        transformed = self.inputImage.transform(
            self.inputImage.size, Image.QUAD,
            [nw[0], nw[1], sw[0], sw[1], se[0], se[1], ne[0], ne[1]],
            Image.BILINEAR)
        (width, height) = transformed.size
        resizeFactor = 4
        self.transformedImage = transformed.resize(
            (width // resizeFactor, height // resizeFactor))

        # try to only retain red pixels
        redMask = Image.new('L', (transformed.size[0], transformed.size[1]))

        for ix in range(transformed.size[0]):
            for iy in range(transformed.size[1]):
                pixel = transformed.getpixel((ix, iy))
                red = pixel[0]
                green = pixel[1]
                blue = pixel[2]
                totalIntensity = red + green + blue
                if totalIntensity == 0:
                    redMask.putpixel((ix, iy), 0)
                else:
                    redProportion = max(0, (red - green) - blue)
                    if redProportion > 10:
                        redMask.putpixel((ix, iy), 255)
                    else:
                        redMask.putpixel((ix, iy), 0)

        self.redMaskImage = redMask
        filePath = 'filtered.jpg'
        redMask.save(filePath)

        completed = subprocess.run(
            [
                "ssocr",
                "invert",
                "-D",  # write a debug file to filePath
                "-T",  # use iteratice thresholding
                "-C",  # omit decimal points
                "-d",  # number of digits in the image, see next parameter
                "-1",  # refers to parameter '-d', -1 stands for 'auto'
                "-c",  # select recognized characters, see next parameter
                "digit",  # refers to parameter '-c', only read digits
                "-t",  # specify threshold, see next parameter
                "25",  # refers to parameter '-t', reshold in %
                filePath
            ],
            stdout=subprocess.PIPE)
        readout = completed.stdout

        report = ''.join(list(filter(lambda x: x != '.', str(readout))))

        self.weight = report[2:4] + '.' + report[4]

        return self.weight

    def showDebugImages(self) -> None:
        """
        Show the image at various stages of transformation for debug purposes
        """
        inputImageSmall = self.inputImage.resize((350, 180))
        ssocrDebugImage = Image.open('testbild.png')

        debugImages = Image.new(mode='RGB',
                                size=(350 * 2, 180 * 2),
                                color='grey')

        debugImages.paste(inputImageSmall, (0, 0))
        debugImages.paste(self.transformedImage, (350, 0))
        debugImages.paste(self.redMaskImage, (0, 180))
        debugImages.paste(ssocrDebugImage, (350, 350))

        debugImages.show()

        debugImageFilePath = (self.archiveFolderName + self.timestamp +
                              '_debug' + self.fileExtension)

        debugImages.save(debugImageFilePath)

        inputImageFilePath = (self.archiveFolderName + self.timestamp +
                              '_original' + self.fileExtension)

        self.inputImage.save(inputImageFilePath)

        os.remove('testbild.png')
