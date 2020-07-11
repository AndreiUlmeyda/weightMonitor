from PIL import Image, ImageChops, ImageDraw
import subprocess
Image.MAX_IMAGE_PIXELS = None

# load image
image = Image.open('scale01.jpg')

# compensate for rotational offset between camera and scale
rotationAngle = 191
rotated = image.rotate(rotationAngle)

# compensate for translational offset between camera and scale
offsetX, offsetY = -100, 400
translated = ImageChops.offset(rotated, offsetX, offsetY)

# approximately crop scale display
cropWidthX, cropWidthY = 500, 500
cropBox = (cropWidthX, cropWidthY, translated.size[0] - cropWidthX, translated.size[0] - cropWidthY)
cropped = translated.crop(cropBox)

# mask with red pixels above threshold
colorChannels = cropped.split()
redChannel = colorChannels[0]

def whiteWhenAboveThreshold(pixelValue):
    threshold = 70
    return (255 if pixelValue > threshold else 0)

#redMask = redChannel.point(whiteWhenAboveThreshold)
redMask = Image.new('L',(cropped.size[0], cropped.size[1]))

for ix in range (cropped.size[0]):
    for iy in range (cropped.size[1]):
        pixel = cropped.getpixel((ix, iy))
        red = pixel[0]
        green = pixel[1]
        blue = pixel[2]
        totalIntensity = red + green + blue
        if totalIntensity == 0:
            redMask.putpixel((ix, iy), 0)
        else:
            redProportion = max(0, (red - green) - blue)
            if redProportion > 0.5:
                redMask.putpixel((ix, iy), redProportion)#int(redProportion*255))
            else:
                redMask.putpixel((ix, iy), redProportion)#int(redProportion*255))

# crop to region containing non-zero pixels
reallyHighNumber = 999999999
topmost, leftmost = reallyHighNumber, reallyHighNumber
bottom, rightmost = 0, 0
maskPixels = redMask.load()
#redMask.show()
redMask.save('herpderp.jpg')
completed = subprocess.run(["ssocr", "invert", "-DT", "-d", "-1", "-c", "digit", "-t", "25", "/home/pi/workspace/weightMonitor/herpderp.jpg"], stdout=subprocess.PIPE)
print(completed.stdout)
outout = completed.stdout.replace(b'b', b'', 1)
command = 'echo %s | festival --tts' % (completed.stdout)
print(command)
subprocess.run(["spd-say", completed.stdout])
#subprocess.run(["echo", completed.stdout, "|", "festival", "--tts"])

for ix in range (redMask.size[0]):
    for iy in range (redMask.size[1]):
        if maskPixels[ix, iy] == 255:
            topmost = min(topmost, iy)
            bottom = max(bottom, iy)
            leftmost = min(leftmost, ix)
            rightmost = max(rightmost, ix)

cropBox = (leftmost, topmost, rightmost, bottom)
nonZeroRegion = redMask.crop(cropBox)

# draw on the image

class Rectangle:
    label = ''
    lengthOfLongSide = 85
    lengthOfShortSide = 10
    
    originX, originY = 0, 0
    lengthX, lengthY = 85, 10
    orientation = 'horizontal'
    color = 'red'
    
    def __init__(self, originX, originY, orientation='horizontal', label = ''):
        self.orientation = orientation
        self.originX = originX
        self.originY = originY
        self.label = label
        self.sideLengthsFromOrientation()
        
    def sideLengthsFromOrientation(self):
        if self.orientation == 'horizontal':
            self.lengthX = self.lengthOfLongSide
            self.lengthY = self.lengthOfShortSide
        else:
            self.lengthX = self.lengthOfShortSide
            self.lengthY = self.lengthOfLongSide
    
    def drawOn(self, image):
        drawable = ImageDraw.Draw(image)        
        oppositeCornerX = self.originX + self.lengthX
        oppositeCornerY = self.originY + self.lengthY
        rectangleCoordinates = [
            self.originX,
            self.originY,
            oppositeCornerX,
            oppositeCornerY
        ]
        
        drawable.rectangle(rectangleCoordinates, outline=self.color)
        drawable.text((self.originX + 2, self.originY), self.label, fill='green')
    
regionAsRGB = nonZeroRegion.convert('RGBA')

horizontal = 'horizontal'
vertical = 'vertical'

rectangleCoordinates = [
        ('1', 40, 5, horizontal),
        ('2', 8, 37, vertical),
        ('3', 157, 34, vertical),
        ('4', 40, 135, horizontal),
        ('5', 18, 158, vertical),
        ('6', 163, 158, vertical),
        ('7', 60, 248, horizontal),
        ('10', 397, 28, vertical),
        ('13', 387, 157, vertical)
]

#for coord in rectangleCoordinates:
#   rectangle = Rectangle(coord[1], coord[2], coord[3], label=coord[0])
#    rectangle.drawOn(regionAsRGB)
