def operation_to_reach(x1,y1,alpha1,x2,y2,alpha2):#what to do ? same code as last year YESS less to do \o/ and this time we don't have to take into account the reverse gear manually that's done by the code.
    if x1==x2 and y1==y2 :
        gamma=alpha2-alpha1
        if gamma>180:
            gamma=gamma-360
        if gamma<-180:
            gamma=gamma+360
        return gamma,0,0
    else :
        s=1
        x=abs(x2-x1)
        y=abs(y2-y1)
        r=int(math.atan2(y,x)*180/math.pi)
        if x!=0 :
            if (x2>=x1 and y2<=y1): 
                r=360-r
            elif y2>=y1 and x2<=x1 :
                r=180-r
            elif (y2<=y1 and x2<=x1):
                r=r+180
        else :
            if (y1<y2) :
                r=90
            else :
                r=270
        rabsolue=r
        
        
        gamma=rabsolue-alpha1#start point
        phy=alpha2-rabsolue
        
        if abs(phy)+abs(gamma)>180:#if we did to much rotation, that's better to reverse the gear (save time)
            gamma=gamma-180#the new angle
            phy=phy-180
            s=-1#set the reverse gear
        
        if (abs(gamma)>180):#this one and the one below are here to make the rotation in the reverse side, same as previously but for the rotation
            gamma=(360-abs(gamma))*((-abs(gamma))/gamma)
            
        if (abs(phy)>180):#
            phy=(360-abs(phy))*((-abs(phy))/phy)
            
        distance=math.sqrt((x*x)+(y*y))*s;
        return gamma,distance,phy


class Motors() :
    def __init__(self) :
        self.state="un_active"
        self.rot1="%"
        self.trans="%"
        self.rot2="%"
        self.done=False
        self.sent=False
        self.warning=False#link with lidar
        self.grab_block=False#link with grab 
    
    def which_state(self) :
        if self.warning!=True :
            if self.state=="un_active":
                self.un_active()
            elif self.state=="rotation1" :
                self.rotation1()
            elif self.state=="translation" :
                self.translation()
            elif self.state=="rotation2" :
                self.rotation2()
        else :
            self.warning
            
    def warning(self) :
        #send an alarm message
        self.rot1="%"
        self.trans="%"
        self.rot2="%"
        self.state="un_active"
        
        
    def un_active(self) :
        if self.rot1!="%" and self.grab_block==False:
            self.state="rotation1"
        
    def rotation1(self) :
        if self.rot1==0 :
            self.done=True
        elif self.sent==False :
            self.sent=True
            print(self.rot1)
            self.rot1="%"
            #we send the order
        if self.done==True:#if done
            self.sent=False
            self.done=False
            if self.trans!="%":
                self.state="translation"
                self.done="%"
            elif self.rot2!="%" :
                self.state="rotation2"
                self.done="%"
            else :
                self.state="un_active"
                self.done="%"
    
    def translation(self) :
        if self.trans==0 :
            self.done=True
        elif self.sent==False :
            self.sent=True
            print(self.trans)
            self.trans="%"
            #we send the order
        if self.done==True:#if done
            self.sent=False
            self.done=False
            if self.rot2!="%":
                self.state="rotation2"
                self.done="%"
            else :
                self.state="un_active"
                self.done="%"        
        
    def rotation2(self) :
        if self.rot2==0:
            self.done=True
        elif self.sent==False :
            print(self.rot2)
            self.rot2="%"
            #we send the order
        if self.done==True:#if done
            self.sent=False
            self.done=False
            self.state="un_active"
            self.done="%" 
    
    def command(self,x,y,alpha,x2,y2,alpha2) :
        print("from",y,alpha,"to",y2,alpha2)
        self.rot1,self.trans,self.rot2=operation_to_reach(x,y,alpha,x2,y2,alpha2)
        print(self.rot1,self.trans,self.rot2)
        
motors=Motors()
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

class Drop_buoy():
    def __init__(self) :
        global motors
        self.state="un_active"
        self.color="%"
        self.order="%"
        self.position="%"
    def which_state(self) :
        if self.state=="un_active":
            self.un_active()
        elif self.state=="su" :
            self.su()
        elif self.state=="r" :
            self.r()
        elif self.state=="ps" :
            self.ps()
        elif self.state=="sh" :
            self.sh()
        elif self.state=="auto" :
            self.auto()
        elif self.state=="po":
            self.po()
            
            
    def un_active(self) :
        global pump,servo,slide
        if self.order=="drop" and self.position!="%" and self.color!="%":
            slide.order="highest"
            self.state="su"
            
    def su(self) :
        global pump,servo,slide
        if slide.done_order==True :
            pump.order="active"
            if self.color=="red" :
                servo.order="right"
                self.state="r"
            elif self.color=="green" :
                servo.order="left"
                self.state="r"
    
    def r(self) :
        global pump,servo,slide
        if self.position==1 :
            slide.order="height_1_placed"
            self.state="ps"
        elif self.position==2 :
            slide.order="height_2_placed"
            self.state="ps"
        elif self.position==3 :
            slide.order="height_2_placed"
            self.state="ps"
    
    def ps(self) :
        global pump,servo,slide
        if slide.done_order==True :
            slide.order="highest"
            servo.order="front"
            self.state="sh"
    
    def sh(self) :
        global pump,servo,slide
        if slide.done_order==True and motors.state=="un_active":
            slide.order="autorization_height"
            self.state="auto"
    
    def auto(self) :
        global pump,servo,slide
        if slide.done_order==True :
            pump.order="reverse"
            self.state="po"
            

        
    def po(self):
        global pump,servo,slide
        pump.order="un_active"
        self.position="%"
        self.color="%"
        self.order="%"
        self.state="un_active"  
            
            
            
            


drop_buoy=Drop_buoy()
class Drop_area() :
    def __init__(self) :
        self.state="active"
        self.drop_x=1800
        self.drop_y=-1600
        self.drop_alpha=270
        self.x=1800
        self.list_position=[[-1750,270-25,"green"],[-1750,270-50,"green"],[-1750,270+25,"red"],[-1750,270+50,"red"],[-1800,270-25,"green"],[-1800,270-50,"green"],[-1800,270+25,"red"],[-1800,270+50,"red"],[-1850,270-25,"green"],[-1850,270-50,"green"],[-1850,270+25,"red"],[-1850,270+50,"red"],[-1940,270-25,"green"],[-1940,270-50,"green"],[-1940,270+25,"red"],[-1940,270+50,"red"]]#list of red withtout the farest last [y,angle,color]
    

            
    def ask(self) :
        if self.state=="active" :
            info=self.list_position.pop()
            if len(self.list_position)==0 :
                self.state="un_active"
            return info
            
        else :
            return ["%","%","%"]
    
drop_area=Drop_area()

class Drop_brain() :
    def __init__(self) :
        self.state="un_active"   
        self.order="%"
        self.operation=["%","%","%"]
        self.stockage_red="%"
        self.stockage_green="%"
        global drop_area
        self.x=drop_area.drop_x
        self.y=drop_area.drop_y
        self.alpha=drop_area.drop_alpha
        self.possible=False

    def which_state(self) :
        if self.state=="un_active":
            self.un_active()
        elif self.state=="check" :
            self.check()
        elif self.state=="active" :
            self.active()
        elif self.state=="change" :
            self.change()
        elif self.state=="go_back":
            self.go_back()
            
    def un_active(self) :
        global drop_area
        if self.order=="drop" :
            self.state="check"
            self.operation=drop_area.ask()
    
    def go_back(self) :
        global motors
        if motors.state=="un_active" :
            self.state="un_active"
            self.order="%"
    
    
    def check(self) :
        global drop_buoy,motors,drop_area
        print(self.stockage_green,self.stockage_red)
        if self.operation==["%","%","%"] or (self.stockage_green==0 and self.stockage_red==0):#if the drop area is full or we don't have anything to put in
            motors.command(self.x,self.y,self.alpha,drop_area.drop_x,drop_area.drop_y,drop_area.drop_alpha)
        
            self.state="go_back"
        else :
            self.possible,drop_buoy.position=self.check_possible(self.operation[2])
            if self.possible==True :
                self.state="active"
                motors.command(self.x,self.y,self.alpha,drop_area.x,self.operation[0],self.operation[1])
                drop_buoy.order="drop"
                drop_buoy.color=self.operation[2]
            else :#if we cannot place something here, give me an over solution
                self.operation=drop_area.ask()
    
    def active(self):
        global drop_buoy,motors,drop_area

        if drop_buoy.order=="%" :
            self.x,self.y,self.alpha=drop_area.x,self.operation[0],self.operation[1]
            if self.operation[2]=="green" :
                self.stockage_green+=-1
            elif self.operation[2]=="red" :
                self.stockage_red+=-1
            self.operation=drop_area.ask()
            self.state="check"
    
    def check_possible(self,color) :
        if color=="green" :
            if self.stockage_green!=0 :
                return True,self.stockage_green
            else :
                return False,"%"
        elif color=="red" :
            if self.stockage_red!=0:
                return True,self.stockage_red
            else :
                return False,"%"
                   
drop_brain=Drop_brain()    
def which_state() :#put grab in last !!
    global grab,pump,servo,slide
    pump.which_state()
    slide.which_state()
    servo.which_state()
    drop_buoy.which_state()
    drop_brain.which_state()
    motors.which_state()
    motors.done=True
    print("slide",slide.state,"servo",servo.state,"pump",pump.state,"drop_buoy",drop_buoy.state,"drop_brain",drop_brain.state,"motors",motors.state)

drop_brain.order="drop"
drop_brain.stockage_green,drop_brain.stockage_red=3,3
while drop_brain.order!="%" :
    which_state()
    