import motor.py
class Lidar() :
    def __init__(self) :
        self.state="un_active"   
        self.order="%"
        self.warning=False
        self.change=False
    def which_state(self) :
        if self.warning!=True :
            if self.state=="un_active":
                self.un_active()
            elif self.state=="check" :
                self.check()
            elif self.state=="warning" :
                self.warning()
            elif self.state=="change" :
                self.change()
        else :
            self.warning
            
    def un_active(self) :
        if self.order=="check" :
            self.state="check"
            self.order="%"
    
    
    def check(self) :
        #check
        if self.warning==True :
            self.state="warning"
        elif self.change==True :
            self.state="change"
        else :
            self.state=="un_active"

    
    def warning(self) :
        #send an alarm message
        self.state="check"
        
        
        
        
        
    def change(self) :
        #change 
        self.state="un_active"
        
        
            
motors=Motors()
import time
motors.command(1,2,3)

while 1 :
    motors.which_state()
    print(motors.state)
    time.sleep(1)
    motors.done="done"
    motors.which_state()
    print(motors.state)
    time.sleep(1)
    motors.done="done"
    motors.which_state()
    print(motors.state)
    time.sleep(1)
    motors.done="done"
    motors.which_state()
    time.sleep(3)
    motors.warning=True
    motors.which_state()
    print(motors.state)


    
        