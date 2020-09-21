class Buoy():
    def __init__(self, color, x,y):
        self.color=color
        self.x = x
        self.y = y
        self.position="%"#position in the storage
        self.color_storage="%"
        self.state="initial"
        self.order="%"
    
    def which_state(self) :#we can direcly apply the function but for the syntax after it will be easier if they have all the same order.
        if self.state=="stocked":
            self.stocked()
        elif self.state=="initial" :
            self.initial()
        #freeze and placed are not flexible
    def initial(self):
        if self.order=="freeze" :
            self.order="%"
            self.state="freeze"
        elif self.order=="stocked":
            global position
            self.x="%"
            self.y="%"
            self.position=position
            self.color_storage=self.color
            self.state="stocked"
            
            
    def stocked(self):
        if self.order=="placed" :
            self.order="%"
            global x_position,y_position
            self.x=x_position
            self.y=y_position
            self.state="placed"
            
        
    
        


buoy=Buoy("green",0,0)
import time
x_position,y_position=1,1
position=0
while 1:
    buoy.which_state()
    print(buoy.state)
    time.sleep(1)  
    buoy.order="placed"
    buoy.which_state()
    print(buoy.state)
    time.sleep(1)
    buoy.order="freeze"

    buoy.which_state()
    print(buoy.state)
    time.sleep(1)
    buoy.order="placed"
    buoy.which_state()
    print(buoy.state)
    time.sleep(1)