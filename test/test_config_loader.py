"""
Unit tests for the class ConfigLoader
"""

import json
import unittest
from unittest.mock import MagicMock
from src.config_loader import ConfigLoader, MissingConfigValuesError


class TestConfigLoader(unittest.TestCase):
    """
    Test that, after loading a json file, all relevant
    values are present before returning a config.
    """
    def setUp(self):
        coordinate = {'x': 2, 'y': 4}
        self.valid_config = {
            'northwest': coordinate,
            'southwest': coordinate,
            'southeast': coordinate,
            'northeast': coordinate
        }

    def test_initialization(self):
        """
        Correct initialization should proceed without raising an exception.
        """
        config_loader = ConfigLoader(json)

        self.assertIsNotNone(config_loader)

    def test_empty_config_object(self):
        """
        If, after loading from a file, an empty json object is returned
        an exception should be raised.
        """
        json.load = MagicMock(return_value={})
        config_loader = ConfigLoader(json)

        self.assertRaises(MissingConfigValuesError, config_loader.get_config)

    def test_missing_corner_config_value(self):
        """
        If an entry for a corner is missing an exception should be raised.
        """
        incomplete_config = self.valid_config
        del incomplete_config['northwest']
        json.load = MagicMock(return_value=incomplete_config)

        config_loader = ConfigLoader(json)

        self.assertRaises(MissingConfigValuesError, config_loader.get_config)

    def test_no_error_with_complete_config(self):
        """
        A valid config should be returned when nothing is missing.
        """
        json.load = MagicMock(return_value=self.valid_config)

        config_loader = ConfigLoader(json)

        self.assertEqual(config_loader.get_config(), self.valid_config)

    def test_missing_coordinate(self):
        """
        Even if a coordinate is only partially missing an exception should be raised.
        """
        incomplete_config = self.valid_config
        del incomplete_config['northwest']['x']
        json.load = MagicMock(return_value=incomplete_config)

        config_loader = ConfigLoader(json)

        self.assertRaises(MissingConfigValuesError, config_loader.get_config)
