from abc import ABC, abstractmethod


class RaspberryInterface(ABC):
    @abstractmethod
    def take_picture(self):
        pass

    @abstractmethod
    def on_button_press(self, action):
        pass
