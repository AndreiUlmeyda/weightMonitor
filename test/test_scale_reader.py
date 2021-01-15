"""
Unit tests for the class ScaleReader
"""
import unittest
from src.scale_reader import ScaleReader, MissingConfigLoaderError


class TestScaleReader(unittest.TestCase):
    """
    The image transformations the class performs are at the
    moment hard to unit test. Instead, it is tested how different
    outputs of the Ocr module with slight errors can still be coerced
    into a useful value
    """
    def test_initialization_missing_config_loader(self):
        """
        An exception should be raised if no ConfigLoader is supplied.
        """
        self.assertRaises(MissingConfigLoaderError,
                          ScaleReader,
                          config_loader=None)
