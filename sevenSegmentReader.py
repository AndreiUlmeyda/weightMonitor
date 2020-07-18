from PIL import Image
import subprocess
import os

class ScaleReader:
    weight = 0
    inputImage = None
    transformedImage = None
    redMaskImage = None
    filteredFilename = 'current_filtered.jpg'
    
    def loadImage(self):
        self.inputImage = Image.open('current.jpg')
        
    def readDigits(self):
        # compensate for rotational offset between camera and scale, rotates counterclockwise
        rotationAngle = 201
        rotated = self.inputImage.rotate(rotationAngle)

        # approximately crop scale display
        cropBox = (335, 245, 690, 420)
        cropped = rotated.crop(cropBox)

        # transform to try and restore horizontal and vertical lines
        nw = (0,0)
        sw = (20,170)
        se = (330, 180)
        ne = (370,0)
        transformed = cropped.transform(cropped.size, Image.QUAD,
                                        [
                                            nw[0],nw[1],sw[0],sw[1],se[0],se[1],ne[0],ne[1]
                                        ],
                                        Image.BILINEAR)
        self.transformedImage = transformed

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

        redMask.save(self.filteredFilename)
        self.redMaskImage = redMask
        currentDirectory = os.getcwd()
        filePath = currentDirectory + '/' +  self.filteredFilename

        completed = subprocess.run(["ssocr", "invert", "-D", "-T", "-C", "-d", "-1", "-c", "digit", "-t", "25", filePath], stdout=subprocess.PIPE)
        readout = completed.stdout

        report = ''.join(list(filter(lambda x: x != '.', str(readout))))

        self.weight = report[2:4] + '.' + report[4]
    
    def textToSpeechTheValue(self):
        text = f"The weight readout is is {self.weight}."
        subprocess.run(["spd-say", text])
        
    def showDebugImages(self):
        debugImage = Image.open('testbild.png')
        debugImages = Image.new(mode='RGBA', size=(350, 180*3), color='grey')
        debugImages.paste(self.transformedImage,(0,0))
        debugImages.paste(self.redMaskImage,(0, 180))
        debugImages.paste(debugImage,(0,360))
        debugImages.show()
        debugImages.save('debugImages.png')
        os.remove('testbild.png')
        os.remove(self.filteredFilename)
        
    def getWeight(self):
        return self.weight




