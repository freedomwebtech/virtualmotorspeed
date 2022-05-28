import cv2
import RPi.GPIO as GPIO
from time import sleep
from cvzone.HandTrackingModule import HandDetector
detector=HandDetector(detectionCon=0.5,maxHands=1)


# Pins for Motor Driver Inputs 
Motor1A = 24
Motor1B = 23
Motor1E = 25

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)              # GPIO Numbering
    GPIO.setup(Motor1A,GPIO.OUT)  # All pins as Outputs
    GPIO.setup(Motor1B,GPIO.OUT)
    GPIO.setup(Motor1E,GPIO.OUT)

def forwards():
    # Going forwards
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
    print("Going forwards")
 

def backwards():
    # Going backwards
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)
    print("Going backwards")
 

def fstop():
    # fstop
    GPIO.output(Motor1E,GPIO.LOW)
    GPIO.output(Motor1A,GPIO.LOW)
    print("fStop")
def bstop():
    #bstop
    GPIO.output(Motor1E,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.LOW)
    print("bStop")
    
def destroy():  
    GPIO.cleanup()    



cap=cv2.VideoCapture(0)

while True:
    ret,frame=cap.read()
    frame=cv2.flip(frame,1)
    hands,frame=detector.findHands(frame)
    if hands:
        setup()
        hands1=hands[0]
        fingers1=detector.fingersUp(hands1)
        count=fingers1.count(1)
        print(fingers1)
        if count == 1:
             forwards()
        elif count==2:
            backwards()
        elif count==3:
             bstop()
             fstop()
        else:
             bstop()
             fstop()
    else:
        print("nohands")
        setup()
        bstop()
        fstop()
            
    frame=cv2.imshow("FRAME",frame)
   
    if cv2.waitKey(1)&0xFF==27:
        break
cap.relase()
cv2.destroyAllWindows()
