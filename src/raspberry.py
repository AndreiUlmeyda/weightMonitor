# pylint: disable=E0401
"""
Provide a class to access Raspberry-Pi capabilities like
detecting button presses and taking images.
"""

import io
from time import sleep
import logging
from src.raspberry_interface import RaspberryInterface
import RPi.GPIO as GPIO
from picamera import PiCamera
from PIL import Image


class Raspberry(RaspberryInterface):
    """
    Prepare and perform actions like taking pictures and reacting to button presses.
    """
    def __init__(self):
        self.pin = 10
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def take_picture(self):
        """
        Take an image using PiCamera
        """
        camera = PiCamera()
        buffer = io.BytesIO()
        camera.capture(buffer, format='jpeg', resize=(1024, 576))
        camera.close()
        buffer.seek(0)
        return Image.open(buffer)

    def loop_and_on_button_press(self, action):
        """
        Wait for a button press. Rule out transient signals on the pin before executing
        the specified action.
        """
        # TODO remove the need for this module to know something about the action it is performing
        logging.info(
            'Please step on the scale to measure and store your weight.')
        while True:
            if self.pin_high():
                if self.pin_high_for_another_while():
                    action()
            sleep(0.1)

    def pin_high_for_another_while(self) -> bool:
        """
        Verify that the pin state is consistently high for consecutive readings
        in order to rule out transient signals.
        """
        pin_state = self.pin_high()
        for _ in range(5):
            pin_state = pin_state and self.pin_high()
            sleep(0.001)
        return pin_state

    def pin_high(self):
        """
        Read the pin state.
        """
        return GPIO.input(self.pin)
