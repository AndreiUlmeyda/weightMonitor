from picamera import PiCamera
from time import sleep
import os

currentDirectory = os.getcwd()

camera = PiCamera()

camera.start_preview()
sleep(8)
camera.stop_preview()

camera.capture(currentDirectory + '/scale04.jpg')
