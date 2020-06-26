import os
from PIL import Image

image = Image.open('scale.jpg')
print (image.format, image.size, image.mode)
image.show()

print 'done'
