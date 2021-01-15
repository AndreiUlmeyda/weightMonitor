"""
Interface to interact with the camera and button press
detection facilities of a raspberry pi.
It is mainly there to allow for a different implementation
to replace Raspberry-Pi specific library calls non-Raspberry-Pi
machines during development.
"""

from abc import ABC, abstractmethod


class RaspberryInterface(ABC):
    """
    Interface for
    """
    @abstractmethod
    def take_picture(self):
        """
        a) accessing a (Raspberry-Pi) camera
        """

    @abstractmethod
    def loop_and_on_button_press(self, action):
        """
        b) calling functions when a button is pressed
        """
