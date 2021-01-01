# pylint: disable=C0103,W0105,C0115,C0116
"""
Small module to load config values from a file.
"""


class MissingConfigValuesError(Exception):
    pass


class ConfigLoader():
    """
    Provide functionality to load config values
    from a file and assure that all required
    keys are present
    """
    def __init__(self, jsonParser):
        self.jsonParser = jsonParser
        self.requiredCornerKeys = [
            'northwest', 'southwest', 'southeast', 'northeast'
        ]
        self.loadedConfig = {}

    def loadConfigFile(self):
        with open('config.json') as file:
            self.loadedConfig = self.jsonParser.load(file)

    def verifyEntriesForEachCorner(self):
        for requiredKey in self.requiredCornerKeys:
            if not requiredKey in self.loadedConfig:
                raise MissingConfigValuesError

    def verifyCoordinatesForEachCorner(self):
        for cornerKey in self.requiredCornerKeys:
            cornerCoordinates = self.loadedConfig[cornerKey]
            xCoordMissing = not 'x' in cornerCoordinates
            yCoordMissing = not 'y' in cornerCoordinates
            if xCoordMissing or yCoordMissing:
                raise MissingConfigValuesError

    def verifyRequiredConfigValues(self):
        self.verifyEntriesForEachCorner()
        self.verifyCoordinatesForEachCorner()

    def getConfig(self):
        self.loadConfigFile()
        self.verifyRequiredConfigValues()

        return self.loadedConfig
