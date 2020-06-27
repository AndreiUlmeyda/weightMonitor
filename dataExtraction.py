import os
from PIL import Image

# load
image = Image.open('scale.jpg')

# rotate
rotationAngle = 195
image = image.rotate(rotationAngle)

# mask for red pixels
imageRGB = image.split()
R,G,B = 0,1,2
threshold = 70
mask = imageRGB[R].point(lambda i: i > threshold and 255)
#mask.show()

topmost, leftmost = 999999, 999999
bottom, rightmost = 0, 0
imagePixels = image.load()
maskPixels = mask.load()
for ix in range (mask.size[0]):
    for iy in range (mask.size[1]):
        if maskPixels[ix, iy]:
            topmost = min(topmost, iy)
            bottom = max(bottom, iy)
            leftmost = min(leftmost, ix)
            rightmost = max(rightmost, ix)

print (topmost, bottom, leftmost, rightmost)
box =(leftmost, topmost, rightmost, bottom)
region = mask.crop(box)
region.show()
