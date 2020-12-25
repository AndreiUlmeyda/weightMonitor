import io
from raspberry import Raspberry
from raspberry_mock import RaspberryMock

def is_raspberrypi():
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            return 'raspberry pi' in m.read().lower()
    except Exception: pass
    return False

class RaspberryFactory():
    def new(self):
        if is_raspberrypi():
            return Raspberry()
        else:
            return RaspberryMock()