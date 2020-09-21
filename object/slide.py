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
list=["highest","height_1_placed","highest","autorization_height"]
m=0
while m!=len(list) or slide.done_order!=True: 
    if slide.done_order==True :
        print(list[m])
        slide.order=list[m]
        m+=1
    slide.which_state()

