from picamera import PiCamera
import RPi.GPIO as GPIO
from time import sleep
from PIL import Image
import requests
import os
from dataExtraction import ScaleReader


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
    weight = scaleReader.getWeight()
    
    requestUrl = f"http://localhost:8086/write?db=sensors"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(requestUrl, data = f"telemetry weight={weight}", headers = headers)
    print(response)
    #scaleReader.showDebugImages()
    
def pinHighForAnotherWhile():
    state = GPIO.input(10)
    for sample in range(5):
        state = state and GPIO.input(10)
        sleep(0.001)
    return state
    
def waitForPinHighStateThenDo(action):
    print("waiting for button...")
    while True:
        if GPIO.input(10):
            if pinHighForAnotherWhile():
                print("button was pressed")
                action()
        sleep(0.1)

waitForPinHighStateThenDo(takePictureReadDigitsSpellThemOut)

