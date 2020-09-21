class Servo() :#maybe this one is too much for nothing
    def __init__(self) :
        self.state="front"
        self.order="%"
    
    def which_state(self) :

        if self.state=="front":
            self.front()
        elif self.state=="right" :
            self.right()
        elif self.state=="left" :
            self.left()

    def front(self) :
        if self.order=="left":
            self.order="%"
            self.state="left"
            self.turn_90()
        elif self.order=="right":
            self.state="right"
            self.order="%"
            self.turn90()
        if self.order=="front":
            self.order="%"#we are already at this state
            
    def right(self) :
        if self.order=="left":#not possible put we do it as if
            self.state="front"
            self.turn_90()#we don't change the order, but it should be in front position at this point
        elif self.order=="right":
            self.order="%"
        if self.order=="front":
            self.order="%"
            self.state="front"
            self.turn_90()
        
    def left(self) :
        if self.order=="left":
            self.oder="%"
        elif self.order=="right":
            self.state="front"
            self.turn90()
        if self.order=="front":
            self.order="%"
            self.state="front"
            self.turn90()
        
    def turn90(self):
        print(90)
    
    def turn_90(self) :
        print(-90)
        
servo=Servo()
import time
while 1 :
    servo.which_state()
    print(servo.state)
    time.sleep(1)
    servo.order="left"
    servo.which_state()
    print(servo.state)
    time.sleep(1)
    servo.order="right"
    servo.which_state()
    print(servo.state)
    time.sleep(1)
    servo.which_state()
    print(servo.state)
    time.sleep(1)
    servo.order='right'
    servo.which_state()
    print(servo.state)
    time.sleep(10)