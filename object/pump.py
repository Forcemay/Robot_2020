class Pump() :
    def __init__(self) :
        self.state="un_active"
        self.order="%"
        
    def which_state(self) :
        if self.state=="un_active":
            self.un_active()
        elif self.state=="active" :
            self.active()
        elif self.state=="reverse" :
            self.reverse()

    def un_active(self) :
        if self.order=="un_active" :
            self.order="%"
        elif self.order=="active" :
            self.state="active"
            print("we active")
            self.order="%"
        elif self.order=="reverse":
            self.state="reverse"
            self.order="%"
            print("we reverse")
        
        
    def active(self) :
        if self.order=="active" :
            self.order="%"
        elif self.order=="un_active" :
            self.state="un_active"
            print("we un_active")
            self.order="%"
        elif self.order=="reverse":
            self.state="reverse"
            self.order="%"
            print("we reverse")
    def reverse(self) :
        if self.order=="reverse" :
            self.order="%"
        elif self.order=="active" :
            self.state="active"
            print("we active")
            self.order="%"
        elif self.order=="un_active" :
            self.state="un_active"
            print("we un_active")
            self.order="%"

pump=Pump()
import time

while 1:
    pump.which_state()
    print(pump.state)
    time.sleep(1)  
    pump.order="active"
    pump.which_state()
    print(pump.state)
    time.sleep(1)
    pump.order="reverse"
    pump.which_state()
    print(pump.state)
    time.sleep(1)
    pump.order="un_active"
    pump.which_state()
    print(pump.state)
    time.sleep(1)
    pump.order="reverse"
    pump.which_state()
    print(pump.state)
    time.sleep(1)