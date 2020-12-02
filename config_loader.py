"""
Small module to load config values from a file.
This is mainly here for testabilities sake
"""

import json

class MissingConfigValuesError(Exception):
    pass

class ConfigLoader():
    def __init__(self, jsonParser):
        self.jsonParser = jsonParser
        self.requiredConfigValues = [
            'northwest',
            'southwest',
            'southeast',
            'northeast'
        ]
        self.loadedConfig = {}

    def loadConfigFile(self):
        with open('config.json') as file:
            self.loadedConfig = self.jsonParser.load(file)

    def verifyRequiredConfigValues(self):
        for requiredKey in self.requiredConfigValues:
            if not requiredKey in self.loadedConfig:
                raise MissingConfigValuesError

    def getConfig(self):
        self.loadConfigFile()
        self.verifyRequiredConfigValues()
        
        return self.loadConfigFile