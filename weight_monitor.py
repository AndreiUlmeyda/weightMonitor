#!/usr/bin/python3
# pylint: disable=C0103,E1101
"""
This module provides a class to transfer measurements from a bathroom scale
into a database.
"""
import io
from time import sleep

import RPi.GPIO as GPIO  # type: ignore
from picamera import PiCamera  # type: ignore
from PIL import Image  # type: ignore
from config_loader import ConfigLoader
import json
from database import Database

from scale_reader import ScaleReader


class WeightMonitor:
    """
    Use a PiCamera to read values of a bathroom scale by taking a picture of
    it and reading the seven segment display when a button is pressed.
    The values are stored using an InfluxDB instance.
    """
    def __init__(self) -> None:
        self.weight = 0
        self.setupPins()

    def setupPins(self) -> None:
        """
        Only one pin is needed to register a button press.
        """
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def imageTheScale(self) -> Image:
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

    def weightFromPictureToDatabase(self) -> None:
        """
        If the button is pressed at the same time as stepping on the scale, then a 7s delay
        is appropriate, for this specific setup, to sync the image with a stable display on
        the scale. Sanity checks are performed, it is assumed that the result of the OCR
        represents a numerical value between 83 and 95 (kg).
        """
        # when hitting the button right when stepping on the scale, the delay
        # of 7 seconds roughly matches the time the camera operates with
        # the time the scale displays the final reading
        sleep(7)
        image = self.imageTheScale()

        # process the image
        configLoader = ConfigLoader(json)
        scaleReader = ScaleReader(image, configLoader)
        readout = scaleReader.readWeight()

        try:
            self.weight = float(readout)
        except ValueError:
            print(
                f"error: readout '{readout}' cannot be interpreted as a number."
            )
            scaleReader.showDebugImages()
            return

        if self.weight < 95 and self.weight > 83:
            error = Database.writeWeight(self.weight)
            if error is None:
                print(
                    f"a weight reading of {self.weight}kg has been commited to the database."
                )
            else:
                print(error)
        else:
            print(f"error: readout '{self.weight}' \
                    is not in the range of assumed values between 83kg and 95kg"
                  )
            scaleReader.showDebugImages()
            return

    def pinHighForAnotherWhile(self) -> bool:
        """
        It needs to be checked that the button state is not transient but
        consistent over multiple measurements during a short while
        """
        state = GPIO.input(10)
        for _ in range(5):
            state = state and GPIO.input(10)
            sleep(0.001)
        return state

    def confirmButtonPressThenDo(self, action):
        """
        A button HIGH state on the button pin can happen randomly.
        It needs to be confirmed that the state is consistent over a short while
        to be sure of a user action.
        """
        if self.pinHighForAnotherWhile():
            print("reading...")
            action()
            self.waitForButtonPressThenDo(action)

    def waitForButtonPressThenDo(self, action):
        """
        The action should only be executed on button press
        """
        print("ready to read weight...")
        while True:
            if GPIO.input(10):
                self.confirmButtonPressThenDo(action)
            sleep(0.1)

    def weightToDatabaseOnButtonPress(self):
        """
        Wait for a button press, then take a picture, read a value from it and commit it to database
        """
        self.waitForButtonPressThenDo(self.weightFromPictureToDatabase)


monitor = WeightMonitor()
monitor.weightToDatabaseOnButtonPress()
