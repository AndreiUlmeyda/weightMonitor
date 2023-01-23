# pylint: disable=C0415
"""
This is a factory class used to instantiate a fake
Raspberry object when it is run on non-Raspberry-Pi
machines. A real Raspberry object would try to
import modules which are not available on the platform,
for instance RPi.GPIO.
"""

import io


class RaspberryFactory:
    """
    A factory to instantiate different objects implementing the RaspberryInterface
    depending on the current platform.
    """
    def __init__(self):
        self.raspberry_model_pattern = 'raspberry pi'
        self.model_info_file_path = '/sys/firmware/devicetree/base/model'

    def new(self):
        """
        Build a fake Raspberry object if the program runs on a non-Raspberry-Pi.
        """
        if self.is_raspberrypi():
            from src.raspberry import Raspberry
            return Raspberry()

        from src.raspberry_mock import RaspberryMock
        return RaspberryMock()

    def is_raspberrypi(self):
        """
        Tries to detect if the current platform is a Raspberry-Pi.
        """
        try:
            with io.open(self.model_info_file_path, 'r') as model_info:
                return self.raspberry_model_pattern in model_info.read().lower(
                )
        except IOError:
            pass
        return False
