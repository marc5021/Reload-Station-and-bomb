#                #
# Reload Station # 
#                #
import RPi.GPIO as GPIO
import time
import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from SessionRequest import *
from GPIO_Setup import *

import os
import sys
currentdir= os.path.dirname(os.path.realpath(__file__))
parentdir= os.path.dirname(currentdir)
sys.path.append(parentdir)
from pn532 import *


GPIO.setwarnings(False)

s = ":"
NFCID = []
Iteration = 0

# Pin of components
GreenLedPin = 4
RedLedPin = 27
buttonPin = 17


#Test function to pretty print data in json format
def Jprint(value):
    print(json.dumps(value,firstIterationindent=4))


def buttonInput(NFCid):
    i = 0
    while i <= 10:
        if not GPIO.input(buttonPin):
            
            try:
                RefillReq(NFCid)
            except:
                print('Failed to reaload, contact supervisor')
            else:
                for iterations in range(10):
                    if iterations % 2 == 0:
                        GPIO.output(GreenLedPin, True)
                        time.sleep(0.5)
                    else:
                        GPIO.output(GreenLedPin, False)
                        time.sleep(0.5)
            print('\nReloaded 100 bullets\n')
            i = 10
        else:
            time.sleep(0.5)
            i = i + 1
                
# Get's information related to the weapon and prints it out
def WeaponInfo(NFCid):
        
    global player
    global product

    weapon = WeaponReq(NFCid).json()
    #Jprint(weapon)

    player = {'name': weapon['player']['name'],
              'bullets': weapon['player']['bullets'],
              'product':weapon['player']['product_id'],
              'team': weapon['player']['team_id'],
              'weapon': weapon['player']['weapon_id']}

    product = {'name': weapon['product']['name'],
               'bullets': weapon['product']['bullets']}


    remainingBullets = int(product['bullets']) - int(player['bullets'])
    
    print("Name: "+player['name'])
    print('Weapon: '+str(player['weapon']))
    #print("Product: "+str(player['product']))
    #print("Team: "+str(player['team']))
    print("Remaning Bullets: "+str(remainingBullets))
    
    if remainingBullets == 0:
        GPIO.output(RedLedPin, True)
        Iteration = 0
    elif remainingBullets > 0:
        GPIO.output(GreenLedPin, True)
        Iteration = 0
        print("\nIf you want to refil, press the button")
        buttonInput(NFCid)
                 
    
    
    
SetupGPIO()

if __name__ == '__main__':
    try:
        pn532 = PN532_UART(debug=False, reset=20)

        ic, ver, rev, support = pn532.get_firmware_version()
        #print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

        # Configure PN532 to communicate with MiFare cards
        pn532.SAM_configuration()

        #print('Waiting for RFID/NFC card...')
        
        while True:
            
            if Iteration == 0:
                print('\nWaiting for RFID/NFC card...')
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=3)
            print('.', end="")
            
            Iteration = Iteration + 1
                      
            # Try again if no card is available.
            if uid is None:
                continue
                
            NFCID = []
            
            IncomeID = [hex(u) for u in uid]
            
            CleanedID = [s.replace('x','') for s in IncomeID]
            
            for id in CleanedID:
                if len(id)>=3 :
                    id = id[1:]
                    NFCID.append(str(id))
                else:
                    NFCID.append(str(id))
            
            NFC_ID = s.join(NFCID)
            
            print(NFC_ID)
            
            try:
                Iteration = 0
                WeaponInfo(NFC_ID)
            except Exception as e:
                print(e)
                Iteration = 0
                GPIO.output(RedLedPin, True)
                #print("No player avalible at given NFC-tag")
                #print("Try again or check with supervisor")
            
            
            time.sleep(3)
            
            GPIO.output(GreenLedPin, False)
            GPIO.output(RedLedPin, False)
            
            

            
            
            #print('Found card with UID:', [hex(i) for i in uid])
           
    except Exception as e:
        print(e)
    finally:
        GPIO.output(GreenLedPin, False)
        GPIO.output(RedLedPin, False)
        GPIO.cleanup()
        
