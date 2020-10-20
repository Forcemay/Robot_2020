
from pump_principal import *
from Slide_principal import *
from motor_principal import *
from Grab_brain_principal import *
from Drop_brain_principal import *
from Brain_principal import *


class Brain():
    def __init__(self):
        self.flat=True
        self.sent=False
        with open('value.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            list = []


            for row in reader:
                if row["Class"]=="Main" :
                    list.append(row["valeur"])
        l1=list[1].split("/")
        l2=list[2].split("/")
        l3=list[3].split("/")
        self.x_grab1,self.y_grab1,self.alpha_grab1=(int(l1[0]),int(l1[1]),int(l1[2]))
        self.x_drop,self.y_drop,self.alpha_drop=(int(l2[0]),int(l2[1]),int(l2[2]))
        self.x_end,self.y_end,self.alpha_end=(int(l3[0]),int(l3[1]),int(l1[2]))
        self.state="ini"



    def which_state(self):
        if self.state == "ini":
            self.ini()
        elif self.state == "grab_position":
            self.grab_position()
        elif self.state == "drop_position":
            self.drop_position()
        elif self.state == "move_grab":
            self.move_grab()
        elif self.state == "move_drop":
            self.move_drop()

    def ini(self):
        global motors
        if self.flag==True:
            self.state="move_grab"
            self.flag=False

    def grab_position(self):
        global grab_brain_principal
        if self.sent==False :
            grab_brain_principal.order="grab1"
            self.sent=True
        elif grab_brain_principal.state=="ini":
            self.state="move_drop"
            self.sent=False

    def drop_position(self):
        global drop_brain_principal
        if self.sent==False :
            drop_brain_principal.order="drop"
            self.sent=True
        elif drop_brain_principal.state=="ini":
            self.state="ini"#finished
            self.sent = False


    def move_grab(self):
        if (motors.x,motors.y,motors.alpha) == (self.x_grab1,self.y_grab1,self.alpha_grab1) :#if done
            self.state = "grab_position"
            self.sent = False

        elif self.sent == False:#if not sent
            motors.command(self.x_grab1,self.y_grab1,self.alpha_grab1)
            self.sent = True

    def move_drop(self):
        if (motors.x, motors.y, motors.alpha) == (self.x_drop,self.y_drop,self.alpha_drop):#if done
            self.state = "drop_position"
            self.sent = False

        elif self.sent == False:#if not sent
            motors.command(self.x_drop,self.y_drop,self.alpha_drop)
            self.sent = True

brain=Brain()




