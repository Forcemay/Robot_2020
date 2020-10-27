
import csv
class Grab_brain_principal():
    def __init__(self,number):
        self.order="%"
        if number==1 :
            self.color=["red","green","red","green","red"]
        else :
            self.color2=["green","red","green","red","green"]
        self.state="un_active"
        with open('value.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            self.list_ini = []
            self.list_grab1=[]
            self.list_change = []
            self.list_grab2=[]
            self.list_end = []
            self.wait=False
            self.wait_list=[]

            self.sent=False
            for row in reader:
                if row["Class"]=="Grab" :
                    if "ini" in row["Nom"] :
                        self.list_ini.append(row["valeur"].split("/"))
                    if "change" in row["Nom"] :
                        self.list_change.append(row["valeur"].split("/"))
                    if "end" in row["Nom"] :
                        self.list_end.append(row["valeur"].split("/"))
                    if "grab1" in row["Nom"] :
                        self.list_grab1.append(row["valeur"].split("/"))
                    if "grab2" in row["Nom"] :
                        self.list_grab2.append(row["valeur"].split("/"))

        self.list_ini.reverse()
        self.list_change.reverse()
        self.list_end.reverse()

    def which_state(self):
        if self.state == "un_active":
            self.un_active()
        elif self.state == "ini":
            self.ini()
        elif self.state == "grab1":
            self.grab1()
        elif self.state == "change":
            self.change()
        elif self.state == "grab2":
            self.grab2()
        elif self.state == "end":
            self.end()
        elif self.state == "fini":
            self.fini()


    def un_active(self):
        if self.order == "un_active":
            self.order = "%"
        elif self.order == "grab":
            self.state = "ini"

    def ini(self):
        global motors
        if len(self.list_ini)>0 and self.wait==False:
            self.wait_list=self.list_ini.pop()
            motors.command(int(self.wait_list[0]),int(self.wait_list[1]),int(self.wait_list[2]))
            self.wait=True
        elif (motors.x, motors.y, motors.alpha)==(int(self.wait_list[0]),int(self.wait_list[1]),int(self.wait_list[2]))
            self.state = "grab1"
            self.wait=False
            list=self.list_grab1[0]
            motors.command(int(list[0]), int(list[1]), int(list[2]))
    def grab1(self):
        if self.sent==False :
            list=self.list_grab1[0]
            self.grab1_object=Grave_move(int(list[0]), int(list[1]), int(list[2]))
            self.grab1_object.order="grab"
            self.sent=True
        else :
            if self.grab1_object.state=="retour" and self.grab1_object.order=="%":
                self.state='change'
                self.sent=False
            else :
                self.grab1_object.which_state()

    def change(self):
        global motors
        if len(self.list_change) > 0 and self.wait==False:
            self.wait=True
            self.wait_list = self.list_change.pop()
            motors.command(int(self.wait_list[0]), int(self.wait_list[1]), int(self.wait_list[2]))
        elif (motors.x, motors.y, motors.alpha)==(int(self.wait_list[0]),int(self.wait_list[1]),int(self.wait_list[2])):
            self.wait=False
            self.state = "grab2"
            list = self.list_grab2[0]
            motors.command(int(list[0]), int(list[1]), int(list[2]))

    def grab2(self):
        if self.sent==False :
            list=self.list_grab2[0]
            self.grab2_object=Grave_move(int(list[0]), int(list[1]), int(list[2]))
            self.grab2_object.order="grab"
            self.sent=True
        else :
            if self.grab2_object.state=="retour" and self.grab2_object.order=="%":
                self.state='change'
                self.sent=False
            else :
                self.grab2_object.which_state()

    def end(self):
        global motors
        if len(self.list_end) > 0 and self.wait==False:
            self.wait=True
            self.wait_list = self.list_end.pop()
            motors.command(int(self.wait_list[0]), int(self.wait_list[1]), int(self.wait_list[2]))
        elif (motors.x, motors.y, motors.alpha) == (int(self.wait_list[0]), int(self.wait_list[1]), int(self.wait_list[2])):
            self.wait=False
            self.state = "fini"
    def fini(self):
        self.order="%"


from ihm_robot import *
col=value_color
if col=="Rouge":
    i=1
else :
    i=2
grab_brain_principal=Grab_brain_principal(i)
