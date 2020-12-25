from raspberry_interface import RaspberryInterface

import RPi.GPIO as GPIO
from picamera import PiCamera
from PIL import Image
import io

class Raspberry(RaspberryInterface):

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def take_picture(self):
        """
        Take a picture of specific size, return it as a PIL.Image
        ! The resolutions when taking pictures for analysis vs taking pictures !
        ! for calibration need to match.                                       !
        """
        camera = PiCamera()
        buffer = io.BytesIO()
        camera.capture(buffer, format='jpeg', resize=(1024, 576))
        camera.close()
        buffer.seek(0)
        return Image.open(buffer)

    def read_pin(self):
       return GPIO.input(10)