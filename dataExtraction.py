from PIL import Image, ImageChops
import subprocess
import os
Image.MAX_IMAGE_PIXELS = None

# load image
image = Image.open('current.jpg')

# compensate for rotational offset between camera and scale
rotationAngle = 191
rotated = image.rotate(rotationAngle)

# TODO update crop and remove translation
# compensate for translational offset between camera and scale
offsetX, offsetY = -100, 400
translated = ImageChops.offset(rotated, offsetX, offsetY)

# approximately crop scale display
cropBox = (330, 000, 680, 180)
cropped = translated.crop(cropBox)

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

# try to only retain red pixels
colorChannels = transformed.split()
redChannel = colorChannels[0]

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

filteredFilename = 'current_filtered.jpg'
redMask.save(filteredFilename)
currentDirectory = os.getcwd()
filePath = currentDirectory + '/' +  filteredFilename

completed = subprocess.run(["ssocr", "invert", "-D", "-T", "-C", "-d", "-1", "-c", "digit", "-t", "25", filePath], stdout=subprocess.PIPE)
readout = completed.stdout
print(readout)

report = ''.join(list(filter(lambda x: x != '.', str(readout))))

report = report[2:4] + '.' + report[4]

print(report)
print(completed.stderr)

subprocess.run(["spd-say", "weight readout"])
subprocess.run(["spd-say", report])

debugImage = Image.open('testbild.png')

debugImages = Image.new(mode='RGBA', size=(350, 180*3), color='grey')
debugImages.paste(transformed,(0,0))
debugImages.paste(redMask,(0, 180))
debugImages.paste(debugImage,(0,360))
debugImages.show()
debugImages.save('debugImages.png')
os.remove('testbild.png')
os.remove(filteredFilename)
