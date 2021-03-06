from time import sleep
# import RPi.GPIO as GPIO

import csv

# GPIO setup
# GPIO.setmode(GPIO.BCM)



class Pump():
    def __init__(self,pin):
        self.color="%"
        self.state = "un_active"
        self.order = "%"
        self.pin=pin
        # GPIO.setup(self.pin, GPIO.OUT)
        # GPIO.output(self.pin, GPIO.HIGH)


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
            print("pump off")
            # GPIO.output(self.pin, GPIO.HIGH)
        else :
            print("pump on")
            # GPIO.output(self.pin, GPIO.LOW)


with open('value.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    l1 = []


    for row in reader:
        if row["Class"]=="Pin" :
            if row["Nom"][0]=="p" :
                l1.append(row["valeur"])
pump1 = Pump(int(l1[0]))
pump2 = Pump(int(l1[1]))
pump3 = Pump(int(l1[2]))
pump4 = Pump(int(l1[3]))
pump5 = Pump(int(l1[4]))