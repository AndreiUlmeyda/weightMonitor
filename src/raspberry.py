from src.raspberry_interface import RaspberryInterface

import RPi.GPIO as GPIO
from picamera import PiCamera
from PIL import Image
import io
from time import sleep
import logging


class Raspberry(RaspberryInterface):
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def take_picture(self):
        camera = PiCamera()
        buffer = io.BytesIO()
        camera.capture(buffer, format='jpeg', resize=(1024, 576))
        camera.close()
        buffer.seek(0)
        return Image.open(buffer)

    def loop_and_on_button_press(self, action):
        # TODO remove the need for this module to know something about the action it is performing
        logging.info('...ready. Please step on the scale at any time to measure and store your weight.')
        while True:
            if self.pinHigh():
                if self.pinHighForAnotherWhile():
                    action()
            sleep(0.1)

    def pinHighForAnotherWhile(self) -> bool:
        pinState = self.pinHigh()
        for _ in range(5):
            pinState = pinState and self.pinHigh()
            sleep(0.001)
        return pinState

    def pinHigh(self):
        return GPIO.input(10)
