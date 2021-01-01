from src.raspberry_interface import RaspberryInterface
from PIL import Image


class RaspberryMock(RaspberryInterface):
    def take_picture(self):
        print('mocked image capture')
        return Image.new(mode='RGB', size=(1024, 768), color=0)

    def on_button_press(self, action):
        print('mocked action')
        action()
