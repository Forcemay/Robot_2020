
import csv
class Drop_brain_principal():
    def __init__(self,number):
        self.move="%"
        self.order="%"
        if number==1 :
            self.color=["red","green","red","green","red"]
        else :
            self.color2=["green","red","green","red","green"]
        self.state="un-active"
        with open('value.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            self.list_ini = []
            self.list_pos1=[]
            self.list_pos2 = []
            self.drop=False

            self.sent=False
            for row in reader:
                if row["Class"]=="Drop" :
                    if "ini" in row["Nom"] :
                        self.list_ini.append(row["valeur"].split("/"))
                    if "pos1" in row["Nom"] :
                        self.list_pop1.append(row["valeur"].split("/"))
                    if "pos2" in row["Nom"] :
                        self.list_pos2.append(row["valeur"].split("/"))


    def which_state(self):
        if self.state == "un_active":
            self.un_active()
        elif self.state == "zone":
            self.zone()
        elif self.state == "move_zone":
            self.move_zone()
        elif self.state == "fini":
            self.fini()


    def un_active(self):
        if self.order == "un_active":
            self.order = "%"
        elif self.order == "drop":
            self.move="zone1"
            self.state = "move_zone"
    def move_zone(self):
        global motors
        if (motors.x, motors.y, motors.alpha) == (self.xmove, self.ymove, self.alphamove):  # if done
            self.state="zone"
            self.sent = False
        elif self.sent == False:  # if not sent
            self.xmove, self.ymove, self.alphamove=self.move_value(self.move)
            motors.command(self.xmove, self.ymove, self.alphamove)
            self.sent = True

    def move_value(self,value):
        if value=="zone1" and value=="zone2" :
            v=self.list_pos1

        elif value=="zone3" and value=="zone4":
            v=self.list_pos2
        else :
            v=self.list_ini

        return int(v[0]),int(v[1]),int(v[2])

    def zone(self):
        if self.sent==False :
            if self.move=="zone1":
                v=self.list_pos1[0]
                self.xmove, self.ymove, self.alphamove = int(v[0]),int(v[1])-100,270
                self.move="zone2"
            if self.move=="zone2":
                self.move = "zone3"
                v=self.list_pos1[0]
                self.xmove, self.ymove, self.alphamove = int(v[0]),int(v[1])+100,270
            if self.move=="zone3":
                self.move = "zone4"
                v=self.list_pos2[0]
                self.xmove, self.ymove, self.alphamove = int(v[0]),int(v[1])-100,90
            if self.move=="zone4":
                self.move = "ini"
                v=self.list_pos2[0]
                self.xmove, self.ymove, self.alphamove = int(v[0]),int(v[1])+100,90

            motors.command(self.xmove, self.ymove, self.alphamove)
            self.sent = True

        if (motors.x, motors.y, motors.alpha) == (self.xmove, self.ymove, self.alphamove):  # if done
            if self.move=="zone2" or self.move=="ini":
                self.slide=slide1
                self.pump=[pump1,pump2,pump3]
            else :
                self.slide=slide2
                self.pump=[pump4,pump5]
            if self.drop == False:
                self.slide.order="low"
                for pump in self.pump :
                    if self.move=="zone2" or self.move=="zone4" :
                        if pump.color=="red":
                            pump.order="un_active"
                    else :
                        if pump.color=="green":
                            pump.order="un_active"
            else :
                self.slide.order='height'
            self.state = "move_zone"
            self.sent = False



drop_brain_principal=Drop_brain_principal()
