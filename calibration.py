from picamera import PiCamera
from PIL import Image, ImageTk
import tkinter as tk
import io

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

window.mainloop()

import json
corners = {}
corners['north-west'] = (0,0)
corners['south-west'] = (20,170)
corners['south-east'] = (33,180)
corners['north-east'] = (370,0)

with open('config.json', 'w') as file:
    json.dump(corners, file, indent = 4)

