from abc import ABC, abstractmethod

class RaspberryInterface(ABC):
    @abstractmethod
    def take_picture(self):
        pass

    @abstractmethod
    def read_pin(self):
        pass