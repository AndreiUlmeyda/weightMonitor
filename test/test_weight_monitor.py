from src.scale_reader import ScaleReader
import unittest
from unittest.mock import MagicMock, patch
from src.weight_monitor import WeightMonitor


class TestWeightMonitor(unittest.TestCase):
    @patch('src.scale_reader.ScaleReader')
    def setUp(self, ScaleReaderMock) -> None:
        self.audio_feedback = MagicMock()
        self.ocr = ScaleReaderMock()
        self.database = MagicMock()
        self.raspberry = MagicMock()
        self.config_loader = MagicMock()
        self.dry_run = False
        self.buildMonitor()

    def buildMonitor(self):
        self.monitor = WeightMonitor(audio_feedback=self.audio_feedback,
                                     scale_reader=self.ocr,
                                     database=self.database,
                                     raspberry=self.raspberry,
                                     config_loader=self.config_loader,
                                     dry_run=self.dry_run)

    def testWritePlausibleWeightToDatabase(self):
        plausibleWeight = 90
        self.ocr.readWeight.return_value = plausibleWeight
        self.buildMonitor()

        self.monitor.weightFromPictureToDatabase()

        self.database.writeWeight.assert_called_once_with(plausibleWeight)
        #self.audio_feedback.success.assert_called_once()
        #TODO add test do differentiate database error

    def testIgnoreImplausibleWeight(self):
        implausibleWeight = 3
        self.ocr.readWeight.return_value = implausibleWeight
        self.buildMonitor()

        self.monitor.weightFromPictureToDatabase()

        self.database.writeWeight.assert_not_called()

    def testIgnorePlausibleWeightOnDryRuns(self):
        plausibleWeight = 90
        self.ocr.readWeight.return_value = plausibleWeight
        self.dry_run = True
        self.buildMonitor()

        self.monitor.weightFromPictureToDatabase()

        self.audio_feedback.success.assert_called_once()
        self.database.writeWeight.assert_not_called()

    def testStartSoundIsPlayed(self):
        self.buildMonitor()

        self.monitor.weightFromPictureToDatabase()

        self.audio_feedback.start.assert_called_once()

    def testUninterpretableReadout(self):
        self.ocr.readWeight.return_value = '?'
        self.buildMonitor()

        self.monitor.weightFromPictureToDatabase()

        self.database.writeWeight.assert_not_called()
        self.audio_feedback.error.assert_called_once()
