from PIL import Image
import subprocess
import os
from datetime import datetime
import json

class ScaleReader:
    weight = 0
    inputImage = None
    transformedImage = None
    redMaskImage = None
    archiveFolderName = 'archive/'
    fileExtension = '.jpg'
    timestamp = None
    
    def __init__(self, image):
        self.inputImage = image
        
    def readWeightFromDisplay(self):
        self.timestamp =  datetime.now().strftime("%Y%m%d%I%M")
        # compensate for rotational offset between camera and scale, rotates counterclockwise
        rotationAngle = 0
        rotated = self.inputImage.rotate(rotationAngle)
        rotated.show()

        # approximately crop scale display
        cropBox = (335, 245, 690, 420)
        cropped = rotated.crop(cropBox)

        # transform to try and restore horizontal and vertical lines
        with open('config.json') as file:
            config = json.load(file)
        
        print(f'config was:\n {config}')
        nw = tuple(config['north-west'])
        sw = tuple(config['south-west'])
        se = tuple(config['south-east'])
        ne = tuple(config['north-east'])

        transformed = self.inputImage.transform(self.inputImage.size, Image.QUAD,
                                        [
                                            nw[0],nw[1],sw[0],sw[1],se[0],se[1],ne[0],ne[1]
                                        ],
                                        Image.BILINEAR)
        (width, height) = transformed.size
        resizeFactor = 4
        self.transformedImage = transformed.resize((width // resizeFactor, height // resizeFactor))

        # try to only retain red pixels
        redMask = Image.new('L',(transformed.size[0], transformed.size[1]))

        for ix in range (transformed.size[0]):
            for iy in range (transformed.size[1]):
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

        completed = subprocess.run(["ssocr", "invert", "-D", "-T", "-C", "-d", "-1", "-c", "digit", "-t", "25", filePath], stdout=subprocess.PIPE)
        readout = completed.stdout

        report = ''.join(list(filter(lambda x: x != '.', str(readout))))

        self.weight = report[2:4] + '.' + report[4]
        
        return self.weight
        
    def showDebugImages(self):
        inputImageSmall = self.inputImage.resize((350,180))
        ssocrDebugImage = Image.open('testbild.png')
        
        debugImages = Image.new(mode='RGB', size=(350*2, 180*2), color='grey')
        
        debugImages.paste(inputImageSmall, (0,0))
        debugImages.paste(self.transformedImage,(350,0))
        debugImages.paste(self.redMaskImage,(0, 180))
        debugImages.paste(ssocrDebugImage,(350,350))
        
        debugImages.show()
        
        debugImageFilePath = self.archiveFolderName + self.timestamp + '_debug' +  self.fileExtension
        debugImages.save(debugImageFilePath)
        inputImageFilePath = self.archiveFolderName + self.timestamp + '_original' +  self.fileExtension
        self.inputImage.save(inputImageFilePath)
        
        os.remove('testbild.png')




