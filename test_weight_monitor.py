from scale_reader import ScaleReader
import unittest
from unittest.mock import MagicMock
from weight_monitor import WeightMonitor


class TestWeightMonitor(unittest.TestCase):
    def setUp(self) -> None:
        audio_feedback = MagicMock()
        ocr = MagicMock()
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
