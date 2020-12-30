from scale_reader import ScaleReader
import unittest
from unittest.mock import MagicMock, patch
from weight_monitor import WeightMonitor
from scale_reader import ScaleReader


class TestWeightMonitor(unittest.TestCase):
    @patch('scale_reader.ScaleReader')
    def setUp(self, ScaleReaderMock) -> None:
        audio_feedback = MagicMock()
        ocr = ScaleReaderMock()
        ocr.readWeight.return_value = 3
        database = MagicMock()
        raspberry = MagicMock()
        config_loader = MagicMock()  # ConfigLoader(json)
        self.monitor = WeightMonitor(audio_feedback=audio_feedback,
                                     scale_reader=ocr,
                                     database=database,
                                     raspberry=raspberry,
                                     config_loader=config_loader,
                                     dry_run=False)

    def testStartStop(self):
        self.monitor.weightFromPictureToDatabase()
