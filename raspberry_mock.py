from raspberry_interface import RaspberryInterface

class RaspberryMock(RaspberryInterface):
    def take_picture(self):
        return None

    def read_pin(self):
        return 0