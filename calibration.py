from picamera import PiCamera
from PIL import Image, ImageTk
import tkinter as tk
import io
import json

camera = PiCamera()
window = tk.Tk()

buffer = io.BytesIO()
camera.capture(buffer, format='jpeg', resize = (1024, 576))
camera.close()
buffer.seek(0)
image = ImageTk.PhotoImage(Image.open(buffer))

width = image.width()
height = image.height()

canvas = tk.Canvas(
        window,
        width = width,
        height = height)

imagePosition = (width / 2, height / 2)
canvas.create_image(imagePosition, image = image)
canvas.pack(fill = tk.BOTH, expand = True)

class Corners:
    cornerIndex = 0
    corners = [(),(),(),()]
    def readCorner(self, event):
        point = (event.x, event.y)
        self.corners[self.cornerIndex] = point
        self.cornerIndex += 1
        self.cornerIndex = self.cornerIndex % 4
        print(self.corners)
    def getConfig(self):
        config = {}
        config['north-west'] = self.corners[0]
        config['south-west'] = self.corners[1]
        config['south-east'] = self.corners[2]
        config['north-east'] = self.corners[3]
        return config

corners = Corners()

def exportConfig(event):
    print("exporting")
    with open('config.json', 'w') as file:
        json.dump(corners.getConfig(), file, indent = 4)
        print("wrote config")
    window.quit()

canvas.bind('<Button-1>', corners.readCorner)
window.bind('<Return>', exportConfig)

window.mainloop()
