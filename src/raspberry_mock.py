from src.raspberry_interface import RaspberryInterface
from PIL import Image
import logging


class RaspberryMock(RaspberryInterface):
    def take_picture(self):
        logging.warn(
            f"Mock module for image capture used. A blank image was provided.")
        return Image.new(mode='RGB', size=(1024, 768), color=0)

    def loop_and_on_button_press(self, action):
        logging.warn(
            f"Mock module for executing an action after a button press used. The action was executed immediately."
        )
        action()
