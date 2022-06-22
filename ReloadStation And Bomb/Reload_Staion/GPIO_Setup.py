# GPIO SETUP for Reload Station

import RPi.GPIO as GPIO

def SetupGPIO():
    
    GPIO.cleanup()
    # Set IO mode
    GPIO.setmode(GPIO.BCM)

    # Pin of components
    GreenLedPin = 4
    RedLedPin = 27
    buttonPin = 17
    # Pin setup
    GPIO.setup(GreenLedPin, GPIO.OUT)
    GPIO.setup(RedLedPin, GPIO.OUT)
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    # Set led to off
    GPIO.output(GreenLedPin, False)
    GPIO.output(RedLedPin, False)