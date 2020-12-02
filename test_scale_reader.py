import unittest
from scale_reader import ScaleReader, MissingInputImageError

class TestScaleReader(unittest.TestCase):
    def testInitialization(self):
        self.assertRaises(MissingInputImageError, ScaleReader, None)
