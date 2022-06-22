#      #
# Bomb # 
#      #
import RPi.GPIO as GPIO
import time
import os
import sys
currentdir= os.path.dirname(os.path.realpath(__file__))
parentdir= os.path.dirname(currentdir)
sys.path.append(parentdir)
from pn532 import *

from SessionRequest import *
from GPIO_Setup import *

GPIO.setwarnings(False)

s = ':'


GreenLedPin = 4
RedLedPin = 27
buttonPin = 17

BombPlanted = False
waiting = True
start = True




def StartTimer():
    i = 30
    
    u = 10
    defusing = 0
    
    while i:
        mins, secs = divmod(i, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        i -= 1
    
        
        if not GPIO.input(buttonPin):
            
            if defusing == 0:
                print('Defusing')
                defusing = 1
            
            for t in range(10):
                
                time.sleep(1)
                
                if not GPIO.input(buttonPin):
                    
                    u = u - 1
                    print(u)
                    
                elif GPIO.input(buttonPin):
                    
                    defusing = 0
                    print('Stopped holding button\n')
                    u = 10
                    break
                
        if u == 0:
            print('Bomb got defused!\n\n')
            GPIO.output(GreenLedPin, True)
            time.sleep(5)
            GPIO.output(GreenLedPin, False)
            main()
        
    else:
        print('BOOOOOOOOMMM!!!\n\n')
        GPIO.output(RedLedPin, True)
        time.sleep(5)
        GPIO.output(RedLedPin, False)
        main()

def PlantBomb():
    waiting = False
    
    i = 0
    uidDetected = 0
    planting = 0
    
    while i != 6:
        
        i = 0
        
        
        uid = pn532.read_passive_target(timeout=0.5)
        
        
        if uid is not None:
            
            if uidDetected == 0:
            
                uidDetected = 1
                print("\nHold button to plant bomb")
                
                
                
        if not GPIO.input(buttonPin) and uid is not None:
            
            if planting == 0:
                print('\nPlanting')
                planting = 1
            
            for i in range(6):
                
                uid = pn532.read_passive_target(timeout=0.5)
                
                if uid is None:
                    planting = 0
                    print('\nBomb was removed from site')
                    break
                
                elif GPIO.input(buttonPin):
                    planting = 0
                    print('\nStopped holding button')
                    break
                
                else:
                    time.sleep(1)
                    i = i + 1
                    print(i)
        
        
        if not GPIO.input(buttonPin) and uid is None:
            print('Bomb needs to be on site')
        # Try again if no card is available.
        if uid is None:
            uidDetected = 0
            planting = 0
            continue
    
    StartTimer()


    

        
def main():
    
    waiting = True
    start = True        
    while True:
                
        if start == True:
            print('Plant bomb on site')
            # Check if a card is available to read
        while waiting == True:
            start = False
            uid = pn532.read_passive_target(timeout=3)
            
                      
                # Try again if no card is available.
            if uid is None:
                continue              
                
            try:
                waiting = False
                PlantBomb()
            except Exception as e:
                print(e)
                
            
SetupGPIO()   

if __name__ == '__main__':
    try:
        pn532 = PN532_UART(debug=False, reset=20)

        ic, ver, rev, support = pn532.get_firmware_version()
        #
        #print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

        # Configure PN532 to communicate with MiFare cards
        pn532.SAM_configuration()
        
    except Exception as e:
        print(e)

    
         
main()
