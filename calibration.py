# pylint: disable=C0103
"""

This script is meant to provide calibration data.
The data represents a tetragonal area of interest specified by the pixel
coordinates of its four corners. The script assumes a functional webcam
equivalent connected to the computer. On startup, it will take a picture
and then allow the user to mark corners using mouse clicks. The first four
clicked locations are written to a JSON file when the export button is clicked.
The reset button will undo all previous clicks.

"""

import tkinter as tk
import io
import json
from picamera import PiCamera
from PIL import Image, ImageTk
from calibrator import Calibrator

CONFIG_FILE_NAME = 'config.json'

ERROR_NO_CAMERA = 'Cannot open webcam'
NOTIFICATION_CALIBRATION_INCOMPLETE = 'Calibration incomplete, not exporting...'
NOTIFICATION_CALIBRATION_COMPLETE = f"Calibration successful, data written to {CONFIG_FILE_NAME}"

BUTTON_LABEL_EXPORT = 'Export Config'
BUTTON_LABEL_RESET_CALIBRATION = 'Reset Calibration'


def takePicture() -> Image:
    """
    Assume a functional webcam. Take a fixed size image and return it in a
    form tkinter expects.
    """
    camera = PiCamera()
    buffer = io.BytesIO()
    camera.capture(buffer, format='jpeg', resize=(1024, 576))
    camera.close()
    buffer.seek(0)
    inputImage = ImageTk.PhotoImage(Image.open(buffer))
    return inputImage


def writeConfig() -> None:
    """
    If calibration was successful, write the config values to a file.
    """
    (calibration, error) = calibrator.getCalibration()
    if error is None:
        with open(CONFIG_FILE_NAME, 'w') as file:
            json.dump(calibration, file, indent=4)
        print(NOTIFICATION_CALIBRATION_COMPLETE)
        window.quit()
    else:
        print(NOTIFICATION_CALIBRATION_INCOMPLETE)


def markCorner(event) -> None:
    """
    Forward the mouse click location to the calibrator.
    """
    calibrator.click(event.x, event.y)


def close(_) -> None:
    """
    Exit the event loop.
    """
    window.quit()


calibrator = Calibrator()

window = tk.Tk()
exportButton = tk.Button(window, text=BUTTON_LABEL_EXPORT, command=writeConfig)
resetButton = tk.Button(window,
                        text=BUTTON_LABEL_RESET_CALIBRATION,
                        command=calibrator.reset)

image = takePicture()
#width, height = image.Image.size
#pprint(vars(image.Image.size))
width = image.width()
height = image.height()

canvas = tk.Canvas(window, background='gray75', width=width, height=height)

# an image position of (0,0) puts the mid point of the image
# at the upper left corner of the frame
imagePosition = (width / 2, height / 2)
canvas.create_image(imagePosition, image=image)

canvas.pack(fill=tk.BOTH, expand=True)
exportButton.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
resetButton.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

canvas.bind('<Button-1>', markCorner)
window.bind('<Escape>', close)

window.mainloop()
