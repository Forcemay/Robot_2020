import math
# import RPi.GPIO as GPIO
import time
#GPIO.cleanup()
# GPIO.setwarnings(False)





class Slide():  # maybe this one is too much for nothing
    def __init__(self,stepPin,dirPin,enPin):
        # change the rotation direction in check_move
        self.stepPin = stepPin
        self.dirPin = dirPin
        self.enPin = enPin
        self.step=1000
        self.height=140
        self.low=100
        self.state="height"
        # order
        self.order = "%"
        # GPIO setup
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(self.enPin,GPIO.OUT)
        # GPIO.setup(self.stepPin,GPIO.OUT)
        # GPIO.setup(self.dirPin,GPIO.OUT)


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
            print("slide up")
            # GPIO.output(dirPin, GPIO.HIGH)
        else :
            print("slide down")
            # GPIO.output(dirPin, GPIO.LOW)
        # for k in range(0, self.step):
        #     GPIO.output(stepPin, GPIO.HIGH)
        #     time.sleep(0.0009)
        #     GPIO.output(stepPin, GPIO.LOW)
        #     time.sleep(0.0009)




#
# slide.order="low"
#
# slide.which_state()
# slide.order="height"
#
# slide.which_state()
