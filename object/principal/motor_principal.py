import math
import csv
import time
def operation_to_reach(x1, y1, alpha1, x2, y2,
                       alpha2):  # what to do ? same code as last year YESS less to do \o/ and this time we don't have to take into account the reverse gear manually that's done by the code.
    if x1 == x2 and y1 == y2:
        gamma = alpha2 - alpha1
        if gamma > 180:
            gamma = gamma - 360
        if gamma < -180:
            gamma = gamma + 360
        return gamma, 0, 0
    else:
        s = 1
        x = abs(x2 - x1)
        y = abs(y2 - y1)
        r = int(math.atan2(y, x) * 180 / math.pi)
        if x != 0:
            if (x2 >= x1 and y2 <= y1):
                r = 360 - r
            elif y2 >= y1 and x2 <= x1:
                r = 180 - r
            elif (y2 <= y1 and x2 <= x1):
                r = r + 180
        else:
            if (y1 < y2):
                r = 90
            else:
                r = 270
        rabsolue = r

        gamma = rabsolue - alpha1  # start point
        phy = alpha2 - rabsolue

        if abs(phy) + abs(gamma) > 180:  # if we did to much rotation, that's better to reverse the gear (save time)
            gamma = gamma - 180  # the new angle
            phy = phy - 180
            s = -1  # set the reverse gear

        if (abs(
                gamma) > 180):  # this one and the one below are here to make the rotation in the reverse side, same as previously but for the rotation
            gamma = (360 - abs(gamma)) * ((-abs(gamma)) / gamma)

        if (abs(phy) > 180):  #
            phy = (360 - abs(phy)) * ((-abs(phy)) / phy)

        distance = math.sqrt((x * x) + (y * y)) * s;
        return gamma, distance, phy


class Motors():
    def __init__(self,x, y, alpha):
        self.state = "un_active"
        self.x, self.y, self.alpha=x, y, alpha
        self.x2, self.y2, self.alpha2 = "%","%","%"
        self.rot1 = "%"
        self.trans = "%"
        self.rot2 = "%"
        self.done = False#for each state
        self.sent = False#for the motor (real)
        self.sent_warning=False
        self.warning = False  # link with lidar
        self.grab_block = False  # link with grab
        self.distance_wears=150
        self.wear=70
        self.step_wear=315
        self.step_mm=self.step_wear/self.wear*3.14
        self.mm_angle=self.distance_wears*3.14/360

    def which_state(self):
        if self.warning != True:
            if self.state == "un_active":
                self.un_active()
            elif self.state == "rotation1":
                self.rotation1()
            elif self.state == "translation":
                self.translation()
            elif self.state == "rotation2":
                self.rotation2()
        else:
            self.state="warning"
            self.warning_state()

    def warning_state(self):
        # send an alarm message
        if self.sent_warning==False:
            #sent warning
            print("sent_warning")
            self.sent_warning=True
        else :
            self.listen_warning()

    def un_active(self):
        if self.rot1 != "%" and self.grab_block == False:
            self.state = "rotation1"

    def rotation1(self):
        self.listen()

        if self.rot1 == 0:
            self.done = True
        elif self.sent == False:
            self.sent = True
            self.speak(self.rot1,'rot')

            # we send the order
        if self.done == True:  # if done
            self.sent = False
            self.done = False
            self.alpha=self.alpha+int(self.rot1)
            self.rot1 = "%"
            if self.trans != "%":
                self.state = "translation"
            elif self.rot2 != "%":
                self.state = "rotation2"
            else:
                self.state = "un_active"
                self.x, self.y, self.alpha=self.x2, self.y2, self.alpha2

    def translation(self):
        self.listen()

        if self.trans == 0:
            self.done = True
        elif self.sent == False:
            self.sent = True
            self.speak(self.trans,'trans')
            # we send the order
        if self.done == True:  # if done
            self.sent = False
            self.done = False
            self.x=self.x2
            self.y=self.y2
            self.trans = "%"

            if self.rot2 != "%":
                self.state = "rotation2"
            else:
                self.state = "un_active"
                self.x, self.y, self.alpha=self.x2, self.y2, self.alpha2


    def rotation2(self):
        self.listen()
        if self.rot2 == 0:
            self.done = True
        elif self.sent == False:
            self.speak(self.rot2,'rot')
            # we send the order
        if self.done == True:  # if done
            self.rot2 = "%"
            self.sent = False
            self.done = False
            self.state = "un_active"
            self.x, self.y, self.alpha = self.x2, self.y2, self.alpha2

    def command(self,x2, y2, alpha2):

        self.rot1, self.trans, self.rot2 = operation_to_reach(self.x, self.y, self.alpha, x2, y2, alpha2)
        self.x2, self.y2, self.alpha2=x2, y2, alpha2
    def speak(self,word,mode):
        word=int(word)
        if mode=="rot":
            message=self.rot_step(word)
        else :
            message=self.trans_step(word)
        print("we sent "+str(message))

    def listen(self):
        #if listen
            #self.done=True
        print("we listen")
        self.done=True
    def listen_warning(self):
    #if receive a message
        #message=""
        #get the number of step
        step=100
        if self.rot1!="%":
            print("rot1",step)
            self.alpha=self.alpha+self.step_rot(step)
            #actu self.rot
        elif self.trans!="%":
            print("trans",step)
            self.trans = self.trans + self.step_trans(step)
        elif self.rot2!="%":
            print("rot2",step)
            self.alpha = self.alpha + self.step_rot(step)
        self.warning=False
        self.sent_warning=False
        self.sent = False
        self.done = False
        self.state="un_active"
    def step_trans(self,step):
        result=step*1/self.step_mm
        return result
    def trans_step(self,mm):
        result=mm*self.step_mm
        return result
    def rot_step(self,angle):
        mm=angle*self.mm_angle
        result=mm*self.step_mm
        return result
    def step_rot(self,step):
        mm=step*1/self.step_mm
        result=mm*1/self.mm_angle
        return result
with open('value.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    list = []


    for row in reader:
        if row["Nom"]=="ini" and row["Class"]=="Main" :
           list.append(row["valeur"])
    l1=list[0].split("/")
motors = Motors(int(l1[0]),int(l1[1]),int(l1[2]))
# motors.command(640,-1600,180)
# while 1:
#     motors.which_state()
#     print(motors.state)
#     time.sleep(1)
#     motors.which_state()
#     print(motors.state)
#     motors.warning = True
#
#     time.sleep(1)
#     motors.which_state()
#     print(motors.state)
#     time.sleep(1)
#     motors.which_state()
#     time.sleep(3)
#     motors.which_state()
#     print(motors.state)
#





