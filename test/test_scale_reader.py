import unittest
from src.scale_reader import ScaleReader, MissingInputImageError, MissingConfigLoaderError
from src.config_loader import ConfigLoader
import json
from PIL import Image


class TestScaleReader(unittest.TestCase):
    def testInitializationMissingConfigLoader(self):
        # image = Image.new(mode='RGB', size=(0, 0))
        self.assertRaises(MissingConfigLoaderError,
                          ScaleReader,
                          configLoader=None)
