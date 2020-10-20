import math
# import RPi.Gpio as Gpio
import time
import csv
# Gpio.cleanup()
# Gpio.setwarnings(False)





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
        # Gpio setup
        # Gpio.setmode(Gpio.BCM)
        # Gpio.setup(self.enPin,Gpio.OUT)
        # Gpio.setup(self.stepPin,Gpio.OUT)
        # Gpio.setup(self.dirPin,Gpio.OUT)


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
            # Gpio.output(dirPin, Gpio.HIGH)
        else :
            print("slide down")
            # Gpio.output(dirPin, Gpio.LOW)
        # for k in range(0, self.step):
        #     Gpio.output(stepPin, Gpio.HIGH)
        #     time.sleep(0.0009)
        #     Gpio.output(stepPin, Gpio.LOW)
        #     time.sleep(0.0009)



with open('value.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    l1 = []


    for row in reader:
        if row["Class"]=="Pin" :
            if row["Nom"][0]=="s" :
                l1.append(row["valeur"])
l2=l1[0].split("/")
l3=l1[1].split("/")
slide1 = Slide(int(l2[0]),int(l2[1]),int(l2[2]))
slide2 = Slide(int(l3[0]),int(l3[1]),int(l3[2]))

