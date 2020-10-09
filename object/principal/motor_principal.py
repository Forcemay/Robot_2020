import math


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
        self.warning = False  # link with lidar
        self.grab_block = False  # link with grab

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
            self.warning

    def warning(self):
        # send an alarm message
        self.rot1 = "%"
        self.trans = "%"
        self.rot2 = "%"
        self.state = "un_active"

    def un_active(self):
        if self.rot1 != "%" and self.grab_block == False:
            self.state = "rotation1"

    def rotation1(self):
        if self.rot1 == 0:
            self.done = True
        elif self.sent == False:
            self.sent = True
            print(self.rot1)
            self.rot1 = "%"
            # we send the order
        if self.done == True:  # if done
            self.sent = False
            self.done = False
            if self.trans != "%":
                self.state = "translation"
                self.done = "%"
            elif self.rot2 != "%":
                self.state = "rotation2"
                self.done = "%"
            else:
                self.state = "un_active"
                self.done = "%"
                self.x, self.y, self.alpha=self.x2, self.y2, self.alpha2

    def translation(self):
        if self.trans == 0:
            self.done = True
        elif self.sent == False:
            self.sent = True
            print(self.trans)
            self.trans = "%"
            # we send the order
        if self.done == True:  # if done
            self.sent = False
            self.done = False
            if self.rot2 != "%":
                self.state = "rotation2"
                self.done = "%"
            else:
                self.state = "un_active"
                self.done = "%"
                self.x, self.y, self.alpha=self.x2, self.y2, self.alpha2


    def rotation2(self):
        if self.rot2 == 0:
            self.done = True
        elif self.sent == False:
            print(self.rot2)
            self.rot2 = "%"
            # we send the order
        if self.done == True:  # if done
            self.sent = False
            self.done = False
            self.state = "un_active"
            self.done = "%"
            self.x, self.y, self.alpha = self.x2, self.y2, self.alpha2

    def command(self,x2, y2, alpha2):

        self.rot1, self.trans, self.rot2 = operation_to_reach(self.x, self.y, self.alpha, x2, y2, alpha2)
        self.x2, self.y2, self.alpha2=x2, y2, alpha2

with open('value.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    list = []


    for row in reader:
        if row["Class"]=="Grab" :
           list.append(row["valeur"])
    l1=list[0].split("/")
motors = Motors(int(l1[0]),int(l1[1]),int(l1[2]))

# while 1:
#     motors.which_state()
#     print(motors.state)
#     time.sleep(1)
#     motors.done = True
#     motors.which_state()
#     print(motors.state)
#     time.sleep(1)
#     motors.done = True
#     motors.which_state()
#     print(motors.state)
#     time.sleep(1)
#     motors.done = True
#     motors.which_state()
#     time.sleep(3)
#     motors.warning = True
#     motors.which_state()
#     print(motors.state)



