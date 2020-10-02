from time import sleep
import RPi.GPIO as GPIO



# GPIO setup
GPIO.setmode(GPIO.BCM)



class Pump():
    def __init__(self,pin):
        self.state = "un_active"
        self.order = "%"
        self.pin=pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH)


    def which_state(self):
        if self.state == "un_active":
            self.un_active()
        elif self.state == "active":
            self.active()

    def un_active(self):
        if self.order == "un_active":
            self.order = "%"
        elif self.order == "active":
            self.state = "active"
            self.pump_action(+1)
            self.order = "%"


    def active(self):
        if self.order == "active":
            self.order = "%"
        elif self.order == "un_active":
            self.state = "un_active"
            self.pump_action(-1)
            self.order = "%"

    def pump_action(self,value):
        if value==-1 :
            GPIO.output(self.pin, GPIO.HIGH)
        else :
            GPIO.output(self.pin, GPIO.LOW)

pump1 = Pump(6)
pump2 = Pump(5)
pump3 = Pump(11)
pump4 = Pump(9)
pump5 = Pump(10)

