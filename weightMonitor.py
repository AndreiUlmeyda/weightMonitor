import subprocess
import io
import RPi.GPIO as GPIO
from time import sleep
from picamera import PiCamera
from PIL import Image
from sevenSegmentReader import ScaleReader

class WeightMonitor:
    weight = 0
    
    def __init__(self):
        self.setupPins()

    def setupPins(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            
    def imageTheScale(self):
        camera = PiCamera()
        buffer = io.BytesIO()
        camera.capture(buffer, format='jpeg', resize=(1024, 576))
        camera.close()
        buffer.seek(0)
        return Image.open(buffer)
        
    def weightFromPictureToDatabase(self):
        # when hitting the button right when stepping on the scale, the delay
        # of 7 seconds roughly matches the time the camera operates with
        # the time the scale displays the final reading
        sleep(7)
        image = self.imageTheScale()
        
        # process the image 
        scaleReader = ScaleReader(image)
        readout = scaleReader.readWeightFromDisplay()
        
        try:
            self.weight = float(readout)
        except ValueError:
            print(f"error: readout '{readout}' cannot be interpreted as a number.")
            scaleReader.showDebugImages()
            return

        if self.weight <95 and self.weight > 83:
            influxLine = f"INSERT telemetry weight={self.weight}"
           # subProcessOutput = subprocess.run(['influx','-database','sensors','-execute', influxLine], stdout=subprocess.PIPE)
            if subProcessOutput.stderr == None:
                print(f"a weight reading of {self.weight}kg has been commited to the database.")
            else:
                print(subProcessOutput.stderr)
        else:
            print(f"error: readout '{self.weight}' is not in the range of assumed values between 83kg and 95kg")
            scaleReader.showDebugImages()
            return
        
    def pinHighForAnotherWhile(self):
        # take 5 quick samples, return true only if all of them are HIGH
        state = GPIO.input(10)
        for sample in range(5):
            state = state and GPIO.input(10)
            sleep(0.001)
        return state

    def confirmButtonPressThenDo(self, action):
        if self.pinHighForAnotherWhile():
            print("reading...")
            action()
            self.waitForButtonPressThenDo(action)

    def waitForButtonPressThenDo(self, action):
        print("ready to read weight...")
        while True:
            if GPIO.input(10):
                self.confirmButtonPressThenDo(action)
            sleep(0.1)
            
    def weightToDatabaseOnButtonPress(self):
        self.waitForButtonPressThenDo(self.weightFromPictureToDatabase)
        
monitor = WeightMonitor()
monitor.weightToDatabaseOnButtonPress()