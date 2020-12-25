#!/usr/bin/python3
# pylint: disable=C0103,E1101
"""
This module provides a class to transfer measurements from
a bathroom scale to a database.
"""
from time import sleep

from PIL import Image
from config_loader import ConfigLoader
from audio_feedback import AudioFeedback
import json
from database import Database
from raspberry_factory import RaspberryFactory

import sys
import threading
from scale_reader import ScaleReader


class WeightMonitor:
    """
    Use a PiCamera to read values off of a bathroom scale by taking a picture of
    it and reading the seven segment display when a button is pressed.
    The values are stored using an InfluxDB instance.
    """
    def __init__(self, dry_run=False) -> None:
        self.dry_run = dry_run
        self.weight = 0
        self.setupPins()
        self.audio = AudioFeedback()
        self.rpi = RaspberryFactory().new()

    def weightFromPictureToDatabase(self) -> None:
        """
        If the button is pressed at the same time as stepping on the scale, then a 7s delay
        is appropriate, for this specific setup, to sync the image with a stable display on
        the scale. Sanity checks are performed, it is assumed that the result of the OCR
        represents a numerical value between 83 and 95 (kg).
        """

        if self.dry_run:
            print("!This is a dry run, nothing will be commited to database!")
        # when hitting the button right when stepping on the scale, the delay
        # of 7 seconds roughly matches the time the camera operates with
        # the time the scale displays the final reading
        sleep(7)
        image = self.rpi.take_picture()

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
            self.audio.error()
            scaleReader.showDebugImages()
            return

        if self.weight < 95 and self.weight > 83:
            error = None
            if not self.dry_run:
                error = Database.writeWeight(self.weight)

            if error is None:
                print(
                    f"a weight reading of {self.weight}kg has been commited to the database."
                )
                self.audio.success()
            else:
                print(error)
                self.audio.error()
        else:
            print(f"error: readout '{self.weight}' \
                    is not in the range of assumed values between 83kg and 95kg"
                  )
            self.audio.error()
            scaleReader.showDebugImages()
            return

    def pinHighForAnotherWhile(self) -> bool:
        """
        It needs to be checked that the button state is not transient but
        consistent over multiple measurements during a short while
        """
        state = self.rpi.read_pin()
        for _ in range(5):
            state = state and self.rpi.read_pin()
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
            self.audio.start()
            threadAction = threading.Thread(target=action)
            threadSoundInProgress = threading.Thread(
                target=self.audio.in_progress)
            threadAction.start()
            threadSoundInProgress.start()
            threadAction.join()
            self.waitForButtonPressThenDo(action)

    def waitForButtonPressThenDo(self, action):
        """
        The action should only be executed on button press
        """
        print("ready to read weight...")
        while True:
            if self.rpi.read_pin():
                self.confirmButtonPressThenDo(action)
            sleep(0.1)

    def weightToDatabaseOnButtonPress(self):
        """
        Wait for a button press, then take a picture, read a value from it and commit it to database
        """
        self.waitForButtonPressThenDo(self.weightFromPictureToDatabase)


dry_run = "-d" in sys.argv or "--dry-run" in sys.argv
monitor = WeightMonitor(dry_run=dry_run)
monitor.weightToDatabaseOnButtonPress()
