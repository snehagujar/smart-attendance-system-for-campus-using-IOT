import os
import hashlib
import sys
import time
import pickle
import socket
import numpy as np
from pyfingerprint.pyfingerprint import PyFingerprint

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = '172.22.35.53'
port = 9998
print ('hello')
s.connect((host, port))
print ('connected')
attendance=[]

print("Enter sub code")
z1 = input(str())
s.send(z1.encode('ascii'))

print("db name")
z2 = input(str())
s.send(z2.encode('ascii'))

print("Enter start time")
z3 = input(str())
s.send(z3.encode('ascii'))

print("Enter end time")
z4 = input(str())
s.send(z4.encode('ascii'))

#initialize the sensor
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

## Getting sensor information
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## searching finger calculate hash
try:
    print('Waiting for finger...')

    ## Waiting finger is read
    while ( f.readImage() == False ):
        pass

    ## Converts read image to characteristics and stores it in charbuffer 1
    f.convertImage(0x01)

    ## Searchs template
    result = f.searchTemplate()

    positionNumber = result[0]
    accuracyScore = result[1]

    if ( positionNumber == -1 ):
        print('No match found!')
        exit(0)
    else:
        print('Found template at position #' + str(positionNumber))
        with open("present_numbers.txt",'a',encoding = 'utf-8') as z:
            z.write(" "+str(positionNumber))
            z.close()
            
        print('The accuracy score is: ' + str(accuracyScore))
        attendance.append(positionNumber)
        print(list(set(attendance)))
        #currentTime =list(set(attendance))
        currentTime1=['1504041','1404031','1404032','1404033']
        data=pickle.dumps(currentTime1)
        s.send(data)

    ## OPTIONAL stuff
    ##

    ## Loads the found template to charbuffer 1
    f.loadTemplate(positionNumber, 0x01)

    ## Downloads the characteristics of template loaded in charbuffer 1
    characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

    ## Hashes characteristics of template
    print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())

except Exception as e:
    print('Operation failed!')
    print('Exception message: ' + str(e))
    exit(1)
