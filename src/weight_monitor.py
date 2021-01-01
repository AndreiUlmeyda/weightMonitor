#!/usr/bin/python3
# pylint: disable=C0103,E1101
"""
This module provides a class to transfer measurements from
a bathroom scale to a database.
"""
from time import sleep

import sys
import threading
import logging


class WeightMonitor:
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

        self.audio.start()

        if self.dry_run:
            logging.info(
                "!This is a dry run, nothing will be commited to database!")
        # when hitting the button right when stepping on the scale, the delay
        # of 7 seconds roughly matches the time the camera operates with
        # the time the scale displays the final reading
        sleep(self.delay)
        image = self.rpi.take_picture()

        # process the image
        readout = self.scale_reader.readWeight(image)

        try:
            self.weight = float(readout)
        except ValueError:
            logging.info(
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
                logging.info(
                    f"a weight reading of {self.weight}kg has been commited to the database."
                )
                self.audio.success()
            else:
                logging.info(error)
                self.audio.error()
        else:
            logging.info(f"error: readout '{self.weight}' \
is not in the range of assumed values between 83kg and 95kg")
            self.audio.error()
            self.scale_reader.showDebugImages()
            return

    def run(self):
        threadWeightToDatabase = threading.Thread(
            target=self.weightFromPictureToDatabase)
        threadSoundInProgress = threading.Thread(target=self.audio.in_progress)
        threadWeightToDatabase.start()
        sleep(1)
        threadSoundInProgress.start()
        threadWeightToDatabase.join()
        self.rpi.on_button_press(self.db.weightFromPictureToDatabase)


if __name__ == "__main__":
    dry_run = "-d" in sys.argv or "--dry-run" in sys.argv
    monitor = WeightMonitor(dry_run=dry_run)
    monitor.run()
