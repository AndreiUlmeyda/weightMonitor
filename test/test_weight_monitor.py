# pylint: disable=W0221
"""
Unit tests for the class WeightMonitor
"""

import unittest
from unittest.mock import MagicMock, patch
from src.weight_monitor import WeightMonitor


class TestWeightMonitor(unittest.TestCase):
    """
    For different outputs of the ScaleReader it is checked whether
    correct values are commited to the database and whether appropriate
    audio feedback is provided.
    """
    @patch('src.scale_reader.ScaleReader')
    def setUp(self, ScaleReaderMock) -> None:
        self.audio_feedback = MagicMock()
        self.ocr = ScaleReaderMock()
        self.database = MagicMock()
        self.raspberry_factory = MagicMock()
        self.dry_run = False
        self.build_monitor()

    def build_monitor(self):
        """
        Build a new weight monitor using the test class variables as
        parameters. This will allow each test to rebuild a WeightMonitor
        using reconfigured mocks.
        """
        self.monitor = WeightMonitor(audio_feedback=self.audio_feedback,
                                     scale_reader=self.ocr,
                                     database=self.database,
                                     raspberry_factory=self.raspberry_factory,
                                     dry_run=self.dry_run)

    def test_write_plausible_weight_to_database(self):
        """
        A plausible weight should be written to the database and
        play a success audio cue.
        """
        plausible_weight = 90
        self.ocr.readWeight.return_value = plausible_weight
        self.database.writeWeight.return_value = None
        self.build_monitor()

        self.monitor.weightFromPictureToDatabase()

        self.database.writeWeight.assert_called_once_with(plausible_weight)
        self.audio_feedback.success.assert_called_once()

    def test_plausible_weight_database_error(self):
        """
        In case of a database error an error audio cue should be played.
        """
        plausible_weight = 90
        self.ocr.readWeight.return_value = plausible_weight
        self.database.writeWeight.return_value = 'some error'
        self.build_monitor()

        self.monitor.weightFromPictureToDatabase()

        self.audio_feedback.error.assert_called_once()

    def test_ignore_implausible_weight(self):
        """
        In case of an implausibly low weight nothing should be commited to database
        and an error audio cue should be played.
        """
        implausible_weight = 3
        self.ocr.readWeight.return_value = implausible_weight
        self.build_monitor()

        self.monitor.weightFromPictureToDatabase()

        self.database.writeWeight.assert_not_called()
        self.audio_feedback.error.assert_called_once()

    def test_ignore_plausible_weight_on_dry_runs(self):
        """
        On dry runs even a plausible weight should not be committed to database.
        """
        plausible_weight = 90
        self.ocr.readWeight.return_value = plausible_weight
        self.dry_run = True
        self.build_monitor()

        self.monitor.weightFromPictureToDatabase()

        self.audio_feedback.success.assert_called_once()
        self.database.writeWeight.assert_not_called()

    def test_start_sound_is_played(self):
        """
        When a reading is initiated a start audio cue should be played.
        """
        self.build_monitor()

        self.monitor.weightFromPictureToDatabase()

        self.audio_feedback.start.assert_called_once()

    def test_uninterpretable_readout(self):
        """
        Garbage output of the ScaleReader should be ignored and
        an error audio cue should be played.
        """
        self.ocr.readWeight.return_value = '?'
        self.build_monitor()

        self.monitor.weightFromPictureToDatabase()

        self.database.writeWeight.assert_not_called()
        self.audio_feedback.error.assert_called_once()
