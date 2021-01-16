#!/usr/bin/python3
# pylint: disable=C0103,E1101,R0913
"""
This module provides a class to transfer measurements from
a bathroom scale to a database.
"""

from time import sleep

import threading
import logging


class WeightMonitor:
    """
    Use Raspberry-Pi capabilities to detect button presses and
    capture images to automate weight monitoring.
    A pressure sensor is used to detect a person stepping on the scale.
    A PiCamera is used to take an image of the scale display.
    OCR is used to read off the value and a local Database is used to store
    the readings.
    Audio feedback is provided to signal start, processing, success/failure.
    """
    def __init__(self,
                 scale_reader,
                 audio_feedback,
                 database,
                 raspberry_factory,
                 delay=0,
                 dry_run=False) -> None:
        self.dry_run = dry_run
        self.weight = 0
        self.audio = audio_feedback
        self.scale_reader = scale_reader
        self.db = database
        self.rpi = raspberry_factory.new()
        self.delay = delay

    def weightFromPictureToDatabase(self) -> None:
        """
        Take a picture and perform OCR on the image.
        If the result passes sanity checks (being a value of the currently possible weight range),
        then store the result in the database.
        If it is a dry run, then do not write anything to database.
        """

        self.audio.start()

        if self.dry_run:
            logging.warning(
                "This is a dry run. Nothing will be commited to database!")
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
            logging.error('Readout %s cannot be interpreted as a number.',
                          readout)
            self.audio.error()
            return

        if self.weight < 95 and self.weight > 83:
            error = None
            if not self.dry_run:
                error = self.db.write_weight(self.weight)

            if error is None:
                logging.info('%skg has been commited to the database.',
                             self.weight)
                self.audio.success()
            else:
                logging.error(error)
                self.audio.error()
        else:
            logging.error(
                'Readout \'%s\' is not in the range of assumed values between 83kg and 95kg',
                self.weight)
            self.audio.error()
            return

    def startAndPlayProgressSound(self):
        """
        Starting the procedure and playing the 'in progress' sound needs
        to happen concurrently in order to make sense.
        """
        threadWeightToDatabase = threading.Thread(
            target=self.weightFromPictureToDatabase)
        threadSoundInProgress = threading.Thread(target=self.audio.in_progress)
        threadWeightToDatabase.start()
        sleep(1.5)
        threadSoundInProgress.start()
        threadWeightToDatabase.join()

    def run(self):
        """
        Let the Raspberry-Pi interface use its capabilities to detect button presses
        start the process.
        """
        self.rpi.loop_and_on_button_press(self.startAndPlayProgressSound)
