
####servo
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

####Pump

class Pump() :
    def __init__(self) :
        self.state="un_active"
        self.order="%"
        
    def which_state(self) :
        if self.state=="un_active":
            self.un_active()
        elif self.state=="active" :
            self.active()
        elif self.state=="reverse" :
            self.reverse()

    def un_active(self) :
        if self.order=="un_active" :
            self.order="%"
        elif self.order=="active" :
            self.state="active"
            print("we active")
            self.order="%"
        elif self.order=="reverse":
            self.state="reverse"
            self.order="%"
            print("we reverse")
        
        
    def active(self) :
        if self.order=="active" :
            self.order="%"
        elif self.order=="un_active" :
            self.state="un_active"
            print("we un_active")
            self.order="%"
        elif self.order=="reverse":
            self.state="reverse"
            self.order="%"
            print("we reverse")
    def reverse(self) :
        if self.order=="reverse" :
            self.order="%"
        elif self.order=="active" :
            self.state="active"
            print("we active")
            self.order="%"
        elif self.order=="un_active" :
            self.state="un_active"
            print("we un_active")
            self.order="%"

pump=Pump()

####Slide
import math

class Slide() :#maybe this one is too much for nothing
    def __init__(self) :
        #change the rotation direction in check_move
        self.state="autorization_height"
        self.autorization_height_data=200
        self.buoy_height_data=115
        self.highest_data=285
        self.height_1_data=170
        #for the placed
        self.height_1_placed_data=130
        self.height_2_placed_data=150
        self.height_3_placed_data=170
        #order
        self.order="%"
        self.done_order=True
        #to split
        self.speed=600#turn/s
        self.step=38/200#mm/step
        self.periode=0.25#periode to split the mouvement in s
        self.current_number=0
        self.step_periode=0
        self.number_periode=0
        
    
    def which_state(self) :

        if self.state=="autorization_height":
            self.autorization_height()
        elif self.state=="buoy_height" :
            self.buoy_height()
        elif self.state=="highest" :
            self.highest()
        elif self.state=="height_1" :
            self.height_1()
        elif self.state=="height_1_placed" :
            self.height_1_placed()
        elif self.state=="height_2_placed" :
            self.height_2_placed()
        elif self.state=="height_3_placed" :
            self.height_3_placed() 

    def autorization_height(self) :
        if self.order=="buoy_height":
            self.several_step(self.autorization_height_data,self.buoy_height_data,"buoy_height")#split the movement if you have to, control by self.done_order
                
                
        elif self.order=="highest":
            self.several_step(self.autorization_height_data,self.highest_data,"highest")

            
    def height_1(self) :
        if self.order=="highest":
            self.several_step(self.height_1_data,self.highest_data,"highest")
            
            
    
    def height_1_placed(self) :
        if self.order=="highest":
            self.several_step(self.height_1_placed_data,self.highest_data,"highest")
            
            
    def height_2_placed(self) :
        if self.order=="highest":
            self.several_step(self.height_2_placed_data,self.highest_data,"highest")
    
    def height_3_placed(self) :
        if self.order=="highest":
            self.several_step(self.height_3_placed_data,self.highest_data,"highest")
            
    def highest(self) :
        if self.order=="height_1" :
            self.several_step(self.highest_data,self.height_1_data,"height_1")

        elif self.order=="height_1_placed" :
            self.several_step(self.highest_data,self.height_1_placed_data,"height_1_placed")

        elif self.order=="height_2_placed" :
            self.several_step(self.highest_data,self.height_2_placed_data,"height_2_placed")

        elif self.order=="height_3_placed" :
            self.several_step(self.highest_data,self.height_3_placed_data,"height_3_placed")
 
        elif self.order=="autorization_height" :
            self.several_step(self.highest_data,self.autorization_height_data,"autorization_height")

    
    def buoy_height(self):
        if self.order=="highest":
            self.several_step(self.buoy_height_data,self.highest_data,"highest")

            
        elif self.order=="autorization_height" :
            self.several_step(self.buoy_height_data,self.autorization_height_data,"autorization_height")

        
        

    def several_step(self,data1,data2,next_step) :
        if self.current_number==0 :
                self.done_order=False #for the communication with outside
                self.step_periode,self.number_periode=self.move_check(data1,data2)#what do we have to do and how many times
        self.move(self.step_periode)#fire
        self.current_number+=1#register that we fire
        if self.current_number==self.number_periode :#if we have fired enough
            self.order="%"
            self.done_order=True #for the communication with outside
            self.current_number=0#important to reset
            self.state=next_step
                

    def move_check(self,bis,zu) :
        print("from",bis,"mm to",zu,"mm")
        have_to_do=-(bis-zu)# if you have to change the rotation direction here
        step_to_do=have_to_do/self.step#in step
        movement_time=step_to_do/self.speed#time
        number_periode=math.ceil(abs((movement_time/self.periode)))#give the number of time we have to fire move to finished the movement, abs because number is positive
        step_periode=int(step_to_do/number_periode)#we can lose some accuracy here, I might admit it but for max 4 step, really ? that's fine, moreover int keep the negativity
        return step_periode,number_periode
    
    def move(self,step) :
        print("we have done",step,"step")

slide=Slide()
        
###end

###main

class Grab_brain():
    def __init__(self) :
        self.state="un_active"
        self.color="%"
        self.order="%"
        self.position="%"
        self.grab_block=False
    def which_state(self) :
        if self.state=="un_active":
            self.un_active()
        elif self.state=="psd" :
            self.psd()
        elif self.state=="auto" :
            self.auto()
        elif self.state=="su" :
            self.su()
        elif self.state=="r" :
            self.r()
        elif self.state=="sd" :
            self.sd()
        elif self.state=="pr" :
            self.pr()
        elif self.state=="suf" :
            self.suf()
        elif self.state=="end":
            self.end()
            
            
    def un_active(self) :
        global pump,servo,slide
        if self.order=="grab" and self.position!="%" and self.color!="%":
            pump.order="active"
            self.grab_block=True
            slide.order="buoy_height"
            self.state="psd"
            
    def psd(self) :
        global pump,servo,slide
        if slide.done_order==True :
            slide.order="autorization_height"
            self.state="auto"
    
    def auto(self) :
        global pump,servo,slide
        if slide.done_order==True :
            self.grab_block=False
            slide.order="highest"
            self.state="su"

    def su(self) :
        global pump,servo,slide
        if slide.done_order==True :
            if self.color=="red" :
                servo.order="right"
                self.state="r"
            elif self.color=="green" :
                servo.order="left"
                self.state="r"
    def r(self) :
        global pump,servo,slide
        if self.position==1 :
            slide.order="height_1"
            self.state="sd"
        elif self.position==2 :
            self.state="sd"
        elif self.position==3 :
            self.state="sd"

    def sd(self) :
        global pump,servo,slide
        if slide.done_order==True :
            pump.order="reverse"
            self.state="pr"
    def pr(self) :
        global pump,servo,slide
        pump.order="un_active"
        servo.order="front"
        slide.order="highest"#if already at highest that will change nothing
        self.state="suf"
    def suf(self) :
        global pump,servo,slide
        if slide.done_order==True :
            slide.order="autorization_height"
            self.state="end"
    def end(self) :
        if slide.done_order==True :
            self.order="%"
            self.color="%"
            self.position="%"
            self.state="un_active"
def which_state() :#put grab in last !!
    global grab,pump,servo,slide
    pump.which_state()
    slide.which_state()
    servo.which_state()
    grab_brain.which_state()
    print("slide",slide.state,"servo",servo.state,"pump",pump.state,"grab_brain",grab_brain.state)

grab_brain=Grab_brain()
grab_brain.order="grab"
grab_brain.color="red"
grab_brain.position=1
while 1:
    which_state()
    