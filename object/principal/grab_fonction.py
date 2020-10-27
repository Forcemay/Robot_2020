from pump_principal import *
from Slide_principal import *
from motor_principal import *

class Grab_move():
    def __init__(self,x,y,alpha):
        global pump1,pump2,pump3,pump4,pump5,slide1,slide2,motors
        self.x=x
        self.y=y
        self.alpha=alpha
        if alpha==0 :
            self.pump=[pump1,pump2,pump3]
            self.slide=slide1
        else :
            self.pump = [pump4, pump5]
            self.slide=slide2
        self.motors=motors
        self.state = "un_active"
        self.order = "%"

    def which_state(self):
        if self.state == "un_active":
            self.un_active()
        elif self.state == "avance":
            self.avance()
        elif self.state == "lever":
            self.lever()
        elif self.state == "retour":
            self.retour()

    def un_active(self):
        if self.order == "un_active":
            self.order = "%"
        elif self.order == "grab":
            self.state = "avance"
            for pump in self.pump :
                pump.order="active"
            self.slide.order="low"
            self.motors.command(self.x-200,self.y,self.alpha)

    def avance(self):
        if (motors.x,motors.y,motors.alpha)==(self.x-200,self.y,self.alpha) :
            self.state = "lever"

            self.slide.order = "height"

    def lever(self):
        self.state = "retour"
        self.motors.command(self.x,self.y,self.alpha)

    def retour(self):
        if (motors.x,motors.y,motors.alpha)==(self.x,self.y,self.alpha) :
            self.order="%"

