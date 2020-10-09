from pump_principal import *
from Slide_principal import *
from motor_principal import *
import csv
class Drop_brain_principal():
    def __init__(self):
        self.order="%"
        self.state="ini"
        self.sent=False
        self.go="%"
        self.counter=1
        with open('value.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            list = []


            for row in reader:
                if row["Class"]=="Drop" :
                    list.append(row["valeur"])
        l1=list[0].split("/")
        l2=list[1].split("/")
        l3=list[2].split("/")
        l4=list[3].split("/")
        l5=list[4].split("/")
        self.x1,self.y1,self.alpha1=int(l1[0]),int(l1[1]),int(l1[2])
        self.x2,self.y2,self.alpha2=int(l2[0]),int(l2[1]),int(l2[2])
        self.x3,self.y3,self.alpha3=int(l3[0]),int(l3[1]),int(l3[2])
        self.x4,self.y4,self.alpha4=int(l4[0]),int(l4[1]),int(l4[2])
        self.xini, self.yini, self.alphaini=int(l5[0]),int(l5[1]),int(l5[2])
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

drop_brain_principal=Drop_brain_principal()


