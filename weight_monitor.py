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
    def __init__(self,
                 scale_reader,
                 audio_feedback,
                 database,
                 raspberry,
                 config_loader,
                 delay=0,
                 dry_run=False) -> None:
        self.dry_run = dry_run
        self.weight = 0
        self.audio = audio_feedback
        self.scale_reader = scale_reader
        self.db = database
        self.rpi = raspberry
        self.config_loader = config_loader
        self.delay = delay

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
        sleep(self.delay)
        image = self.rpi.take_picture()

        # process the image
        readout = self.scale_reader.readWeight()

        try:
            self.weight = float(readout)
        except ValueError:
            print(
                f"error: readout '{readout}' cannot be interpreted as a number."
            )
            self.audio.error()
            self.scale_reader.showDebugImages()
            return

        if self.weight < 95 and self.weight > 83:
            error = None
            if not self.dry_run:
                error = self.db.writeWeight(self.weight)

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
is not in the range of assumed values between 83kg and 95kg")
            self.audio.error()
            self.scale_reader.showDebugImages()
            return

    def run(self):
        self.rpi.on_button_press(self.db.weightFromPictureToDatabase)


if __name__ == "__main__":
    dry_run = "-d" in sys.argv or "--dry-run" in sys.argv
    monitor = WeightMonitor(dry_run=dry_run)
    monitor.run()
