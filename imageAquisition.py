from picamera import PiCamera
import RPi.GPIO as GPIO
from time import sleep
from PIL import Image
import subprocess
import os
from sevenSegmentReader import ScaleReader


currentDirectory = os.getcwd()
filename = '/current.jpg'

GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

weight = 0
        
def takeAPicture():
    camera = PiCamera()
    camera.capture(currentDirectory + filename, resize=(1024, 576))
    camera.close()
    
def showThePicture():
    image = Image.open('current.jpg')
    image.show()

def takeAndShowPicture():
    takeAPicture()
    showThePicture()
    
def takePictureReadDigitsSpellThemOut():
    sleep(7)
    
    takeAPicture()
    
    scaleReader = ScaleReader()
    scaleReader.loadImage()
    scaleReader.readDigits()
    scaleReader.textToSpeechTheValue()
    weight = 0
    try:
        weight = float(scaleReader.getWeight())
    except ValueError:
        print(f"error: readout '{scaleReader.getWeight()}' cannot be interpreted as a number.")
        return

    if weight <95 and weight > 83: 
        influxLine = f"INSERT telemetry weight={weight}"
        subProcessOutput = subprocess.run(['influx','-database','sensors','-execute', influxLine], stdout=subprocess.PIPE)
        if subProcessOutput.stderr != None:
            print(subProcessOutput.stderr)
    else:
        print(f"error: readout '{weight}' is not in the range of assumed values between 83kg and 95kg")
        return

    scaleReader.showDebugImages()
    
def pinHighForAnotherWhile():
    state = GPIO.input(10)
    for sample in range(5):
        state = state and GPIO.input(10)
        sleep(0.001)
    return state
    
def waitForPinHighStateThenDo(action):
    print("ready to read weight when button is pressed...")
    while True:
        if GPIO.input(10):
            if pinHighForAnotherWhile():
                print("reading...")
                action()
                waitForPinHighStateThenDo(action)
        sleep(0.1)

waitForPinHighStateThenDo(takePictureReadDigitsSpellThemOut)

