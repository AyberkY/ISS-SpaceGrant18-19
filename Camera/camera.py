from picamera import PiCamera
from time import sleep

cam = PiCamera()  

def accelMEASURE():                 #defines a function that takes Ayush function and makes it check if the camera should happen
    currentACCEL = ayushFUNCTION(-1)
    pastACCEL = ayushFUNCTION(-10)
    
    avgACCEL = (abs(currentACCEL) + abs(pastACCEL))/2
    return avgACCEL


def cameraRECORD():                      #function that does the camera
    flightSTATUS = 1                     #flight is happening
    accelCHECK = accelMEASURE()
    
    cam.start_recording('path...')      #starts recording
    
    while flightSTATUS == 1:            #check if rocket is in flight
        sleep(10)
        if accelCHECK <= 10**-2:
            flightSTATUS -= 1
        else:
            continue
        
    cam.stop_recording()                #stops recording

cameraRECORD()


    



