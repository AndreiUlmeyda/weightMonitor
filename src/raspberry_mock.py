"""
This class is used to fake the functionality of
a Raspberry-Pi when the program is run on non-Raspberry-Pi
machines.
"""

import logging
from src.raspberry_interface import RaspberryInterface
from PIL import Image


class RaspberryMock(RaspberryInterface):
    """
    Fake the actions of:
    """
    def take_picture(self):
        """
        a) producing an image using a Raspberry-Pi camera by returning
           a blank image of the right size.
        """
        logging.warning(
            'Mock module for image capture used. A blank image was provided.')
        return Image.new(mode='RGB', size=(1024, 768), color=0)

    def loop_and_on_button_press(self, action):
        """
        b) executing an action based on a button press by executing it
           immediately.
        """
        logging.warning(
            'Mock module for executing an action after a button press used. \
                The action was executed immediately.')
        action()
