import unittest
from src.config_loader import ConfigLoader, MissingConfigValuesError
import json
from unittest.mock import MagicMock


class TestConfigLoader(unittest.TestCase):
    def setUp(self):
        coordinate = {'x': 2, 'y': 4}
        self.validConfig = {
            'northwest': coordinate,
            'southwest': coordinate,
            'southeast': coordinate,
            'northeast': coordinate
        }

    def testInitialization(self):
        config_loader = ConfigLoader(json)

        self.assertIsNotNone(config_loader)

    def testEmptyConfigObject(self):
        json.load = MagicMock(return_value={})
        config_loader = ConfigLoader(json)

        self.assertRaises(MissingConfigValuesError, config_loader.getConfig)

    def testMissingCornerConfigValue(self):
        incompleteConfig = self.validConfig
        del incompleteConfig['northwest']
        json.load = MagicMock(return_value=incompleteConfig)

        config_loader = ConfigLoader(json)

        self.assertRaises(MissingConfigValuesError, config_loader.getConfig)

    def testNoErrorWithCompleteConfig(self):
        json.load = MagicMock(return_value=self.validConfig)

        config_loader = ConfigLoader(json)

        self.assertEqual(config_loader.getConfig(), self.validConfig)

    def testMissingCoordinate(self):
        incompleteConfig = self.validConfig
        del incompleteConfig['northwest']['x']
        json.load = MagicMock(return_value=incompleteConfig)

        config_loader = ConfigLoader(json)

        self.assertRaises(MissingConfigValuesError, config_loader.getConfig)
