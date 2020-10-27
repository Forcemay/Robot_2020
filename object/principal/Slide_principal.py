import math
import RPi.GPIO as GPIO
import time
#GPIO.cleanup()
GPIO.setwarnings(False)

stepPin = 13
dirPin = 19
enPin = 26

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(enPin,GPIO.OUT)
GPIO.setup(stepPin,GPIO.OUT)
GPIO.setup(dirPin,GPIO.OUT)

class Slide():  # maybe this one is too much for nothing
    def __init__(self):
        # change the rotation direction in check_move
        self.step=1000
        self.height=140
        self.low=100
        self.state="height"
        # order
        self.order = "%"


    def which_state(self):

        if self.state == "height":
            self.height_state()
        elif self.state == "low":
            self.low_state()


    def height_state(self):
        if self.order == "low":
            self.move(-1)
            self.state="low"


    def low_state(self):
        if self.order == "height":
            self.move(+1)
            self.state="height"



    def move(self, value):
        if value==1:
            GPIO.output(dirPin, GPIO.HIGH)
        else :
            GPIO.output(dirPin, GPIO.LOW)
        for k in range(0, self.step):
            GPIO.output(stepPin, GPIO.HIGH)
            time.sleep(0.0009)
            GPIO.output(stepPin, GPIO.LOW)
            time.sleep(0.0009)




slide = Slide()

slide.order="low"

slide.which_state()
slide.order="height"

slide.which_state()
