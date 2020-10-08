from pump_principal import *
from Slide_principal import *
from motor_principal import *

class Grab_brain_principal():
    def __init__(self,number):
        self.order="%"
        if number==1 :
            self.color=["red","green","red","green","red"]
        else :
            self.color2=["green","red","green","red","green"]
        self.state="ini"
        self.counter1=0
        self.grab1_action=[(1, -1, 10, 0, 0),(1, 1, 10, 0, 0),(1, 1, 0, 0, -180),(1, -1, 10, 0, -180),(1, -1, 10, 0, -180),(1, 1, 0,0,0)]
        self.counter2=0

    def which_state(self) :
        if self.state=="ini":
            self.ini()
        elif self.state=="grab1" :# il would be rather more interresting to but every operation one after the other instead of building a useless state graph
            self.grab1()
        elif self.state=="grab2":
            self.grab2()

    def ini(self):
        if self.order=="grab1":

            self.order="%"
            self.state="grab1"
        elif self.order=="grab2":
            self.order="%"
            self.state = "grab2"

    def grab1(self):
        global motors
        if self.order!='ini' and motors.state=="un_active":
            if self.counter1<len(self.grab1_action) :
                pump_order, slide_order, x, y, alpha=self.grab1_action[self.counter1]
                self.action(pump_order, slide_order, x, y, alpha)
                self.counter1=self.counter1+1
            else :
                self.state='ini'
                self.counter1=0
                self.order="%"


    def grab2(self):
        global motors
        if self.order != 'ini'and motors.state=="un_active":
            if self.counter2 < len(self.grab2_action):
                pump_order, slide_order, x, y, alpha = self.grab2_action[self.counter1]
                self.action(pump_order, slide_order, x, y, alpha)
                self.counter2 = self.counter2 + 1
            else :
                self.state='ini'
                self.counter2
                self.order="%"


    def action(self,pump_order,slide_order,x,y,alpha):
        global slide1,slide2,pump1,pump2,pump3,pump4,pump5
        pump_list=[]
        if self.counter1<3 :
            slide=slide1
            pump_list.append(pump1)
            pump1.color=self.color[0]
            pump_list.append(pump2)
            pump2.color = self.color[1]
            pump_list.append(pump3)
            pump3.color = self.color[2]
        else :
            slide=slide2
            pump_list.append(pump4)
            pump4.color = self.color[3]
            pump_list.append(pump5)
            pump5.color = self.color[4]
        if pump_order==1 :
            for i in pump_list :
                i.order="active"
        else :
            for i in pump_list :
                i.order="un_active"
        if slide_order==1 :
            slide.order="height"
        else :
            slide.order="low"
        if x!=motors.x or y!=motors.y or alpha!=motors.alpha :
            motors.command(x,y,alpha)


class Drop_brain_principal():
    def __init__(self):
        self.order="%"
        self.state="ini"
        self.sent=False
        self.go="%"
        self.counter=1
        self.x1,self.y1,self.alpha1=(10,10,0)
        self.x2,self.y2,self.alpha2=(10,-10,180)
        self.x3,self.y3,self.alpha3=(20,10,0)
        self.x4,self.y4,self.alpha4=(20,-10,180)
        self.xini, self.yini, self.alphaini = (30, 0, -90)
        self.xmove,self.ymove,self.alphamove=(0,0,0)
    def which_state(self) :
        if self.state=="ini":
            self.ini()
        elif self.state=="move" :
            self.move()
        elif self.state=="zone" :
            self.zone()

    def ini(self):
        if self.order=="drop":
            self.order="%"
            self.state="move"
            self.go="zone1"
            self.xmove, self.ymove, self.alphamove=(self.x1,self.y1,self.alpha1)
    def zone(self):
        global pump1,pump2,pump3,pump4,pump5,slide1,slide2
        if self.go=='zone1' or self.go=="zone4":
            slide=slide1
            list=[pump1,pump2,pump3]
        elif self.go=='zone2' or self.go=="zone3":
            slide=slide2
            list=[pump4,pump5]
        if self.go=='zone1' or self.go=="zone3":
            color="red"
        elif self.go=='zone2' or self.go=="zone4":
            color="green"
        print(self.counter)
        if self.counter==1 :
            slide.order="low"
            self.counter=self.counter+1
            for p in list :
                if p.color==color :
                    p.order="un_active"

        elif self.counter==2 :
            slide.order="height"
            self.counter=self.counter+1
        elif self.counter==3 :
            self.counter=1
            if self.go=="zone1":
                self.go="zone2"
                self.xmove, self.ymove, self.alphamove = (self.x2, self.y2, self.alpha2)
            elif self.go=="zone2":
                self.xmove, self.ymove, self.alphamove = (self.x3, self.y3, self.alpha3)
                self.go="zone3"
            elif self.go=="zone3":
                self.xmove, self.ymove, self.alphamove = (self.x4, self.y4, self.alpha4)
                self.go="zone4"
            elif self.go=="zone4":
                self.xmove, self.ymove, self.alphamove = (self.xini, self.yini, self.alphaini)
                self.go="ini"
            self.state="move"




    def move(self):
        global motors
        if (motors.x, motors.y, motors.alpha) == (self.xmove, self.ymove, self.alphamove):  # if done
            if (motors.x, motors.y, motors.alpha)==(self.xini, self.yini, self.alphaini) :
                self.state="ini"
            else :
                self.state="zone"
            self.sent = False

        elif self.sent == False:  # if not sent
            motors.command(self.xmove, self.ymove, self.alphamove)
            self.sent = True


class Brain():
    def __init__(self):
        self.flat=True
        self.sent=False
        self.x_grab1,self.y_grab1,self.alpha_grab1=(400,-1600,-90)
        self.x_drop,self.y_drop,self.alpha_drop=(450,-800,-90)
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
        print("ici")
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

motors = Motors(200, -800, 90)
pump1 = Pump(6,1)
pump2 = Pump(5,1)
pump3 = Pump(11,1)
pump4 = Pump(9,2)
pump5 = Pump(10,2)
slide1 = Slide(13,19,26)
slide2 = Slide(13,19,26)
drop_brain_principal=Drop_brain_principal()
grab_brain_principal=Grab_brain_principal(1)
brain=Brain()

def which_state_global():
    l=[brain,drop_brain_principal,grab_brain_principal,slide1,slide2,pump1,pump2,pump3,pump4,pump5,motors]
    for s in l :
        s.which_state()

brain.flag=True
while 1:
    which_state_global()
    motors.done=True


