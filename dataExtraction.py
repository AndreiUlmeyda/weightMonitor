from PIL import Image, ImageChops, ImageDraw

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

redMask = redChannel.point(whiteWhenAboveThreshold)

# crop to region containing non-zero pixels
reallyHighNumber = 999999999
topmost, leftmost = reallyHighNumber, reallyHighNumber
bottom, rightmost = 0, 0
maskPixels = redMask.load()

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
def drawRectangle(img, x0, y0, x1, y1):
    draw = ImageDraw.Draw(img)
    draw.rectangle([x0,y0,x1,y1], outline='red')
    
regionAsRGB = nonZeroRegion.convert('RGBA')
drawRectangle(regionAsRGB, 40, 5, 125, 15)

regionAsRGB.show()
