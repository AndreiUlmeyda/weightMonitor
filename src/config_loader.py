# pylint: disable=C0103,W0105,C0115,C0116
"""
Small module to load config values from a file.
"""


class MissingConfigValuesError(Exception):
    pass


class ConfigLoader:
    """
    Provide functionality to load config values
    from a file and assure that all required
    keys are present
    """
    def __init__(self, json_parser):
        self.jsonParser = json_parser
        self.requiredCornerKeys = [
            'northwest', 'southwest', 'southeast', 'northeast'
        ]
        self.loadedConfig = {}

    def load_config_file(self):
        with open('config.json') as file:
            self.loadedConfig = self.jsonParser.load(file)

    def verify_entries_for_each_corner(self):
        for requiredKey in self.requiredCornerKeys:
            if requiredKey not in self.loadedConfig:
                raise MissingConfigValuesError

    def verify_coordinates_for_each_corner(self):
        for cornerKey in self.requiredCornerKeys:
            corner_coordinates = self.loadedConfig[cornerKey]
            x_coord_missing = 'x' not in corner_coordinates
            y_coord_missing = 'y' not in corner_coordinates
            if x_coord_missing or y_coord_missing:
                raise MissingConfigValuesError

    def verify_required_config_values(self):
        self.verify_entries_for_each_corner()
        self.verify_coordinates_for_each_corner()

    def get_config(self):
        self.load_config_file()
        self.verify_required_config_values()

        return self.loadedConfig
