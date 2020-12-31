from scale_reader import ScaleReader
import unittest
from unittest.mock import MagicMock, patch
from weight_monitor import WeightMonitor
from scale_reader import ScaleReader


class TestWeightMonitor(unittest.TestCase):
    @patch('scale_reader.ScaleReader')
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

    def testWritePlausibleWeightsToDatabase(self):
        plausibleWeight = 90
        self.ocr.readWeight.return_value = plausibleWeight
        self.buildMonitor()

        self.monitor.weightFromPictureToDatabase()

        self.database.writeWeight.assert_called_once_with(plausibleWeight)

    def testIgnoreImplausibleWeights(self):
        implausibleWeight = 3
        self.ocr.readWeight.return_value = implausibleWeight
        self.buildMonitor()

        self.monitor.weightFromPictureToDatabase()

        self.database.writeWeight.assert_not_called()

    def testIgnorePlausibleWeightsOnDryRuns(self):
        plausibleWeight = 90
        self.ocr.readWeight.return_value = plausibleWeight
        self.dry_run = True
        self.buildMonitor()

        self.monitor.weightFromPictureToDatabase()

        self.database.writeWeight.assert_not_called()
