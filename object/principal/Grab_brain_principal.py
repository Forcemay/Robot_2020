from pump_principal import *
from Slide_principal import *
from motor_principal import *
import csv
class Grab_brain_principal():
    def __init__(self,number):
        self.order="%"
        if number==1 :
            self.color=["red","green","red","green","red"]
        else :
            self.color2=["green","red","green","red","green"]
        self.state="ini"
        self.counter1=0
        with open('value.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            list = []


            for row in reader:
                if row["Class"]=="Grab" :
                    list.append(row["valeur"])
        l1=list[0].split("/")
        l2=list[1].split("/")
        l3=list[2].split("/")
        l4=list[3].split("/")
        self.grab1_action=[(1, -1, int(l1[0]),int(l1[1]),int(l1[2])),(1, 1,int(l1[0]),int(l1[1]),int(l1[2])),(1, 1, int(l2[0]),int(l2[1]),int(l2[2])),(1, -1, int(l3[0]),int(l3[1]),int(l3[2])),(1, -1, int(l3[0]),int(l3[1]),int(l3[2])),(1, 1, int(l4[0]),int(l4[1]),int(l4[2]))]
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


from ihm_robot import *
col=value_color
if col=="Rouge":
    i=1
else :
    i=2
grab_brain_principal=Grab_brain_principal(i)
