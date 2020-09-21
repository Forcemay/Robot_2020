import time as temps
def main_think(buoy_available,objectif,x,y,alpha) :
    for x in objectif :
        x.append("buoy")
    return objectif
class main_brain() :
    def __init__(self,strategy_selection) :
        self.strategy_selection=strategy_selection#have to be defined, list
        if self.strategy_selection=="sweet" :
            self.strategy_list=[[[Z]],[[D],[E],[F]],[[E]],[[E]],[[A],[B],[C]]]
        elif self.strategy_selection=="normal" :
            self.strategy_list=[[[Z]],[[D],[E],[F]],[[E]],[[E]],[[A],[B],[C]]]
        elif self.strategy_selection=="ballsy" :
            self.strategy_list=[[[Z]],[[D],[E],[F]],[[E]],[[E]],[[A],[B],[C]]]
        self.warning=0
        self.change=False
        self.objective_overview=[]
        self.objective=[]
        self.buoy_available=[]
        self.the_issue_x="%"
        self.the_issue_y="%"
        self.x="%"
        self.y="%"
        self.alpha="%"
        self.goal="%"
        self.chck=0
        self.wchck=0
        self.warning_time="%"
        self.come_back="%"
    
    
    def which_state(self) :
        if self.state=="strategy":
            self.strategy()
        elif self.state=="think" :
            self.think()
        elif self.state=="check" :
            self.check()
        elif self.state=="warning" :
            self.warning()
        elif self.state=="control":
            self.control()
        elif self.state=="move":
            self.move()
        
    
    def strategy(self) :
        if len(self.objective_overview)==0 :
            self.objective_overview=main_think(buoy_available,strategy_list.pop(),self.x,self.y,self.alpha)
        self.objective=self.objective_overview.pop()
        
    def think(self) :
        x=round(self.goal.history[0][0])
        y=round(self.goal.history[0][1])
        alpha=round(self.goal.history[0][2])
        motors.command(self.x,self.y,self.alpha,x,y,alpha)
        self.state="check"
    def check(self) :
        #will return new x,y,alpha and the constraints 
        if self.come_back=="nothing" :#if no issues
            if motors.state=="un_active" :#no command
                self.warning=0
                self.state="control"#let's check what we sould do next
            elif self.warning==1 :#if there were a warning (problem is gone) just 
                self.come_back="change"
    
                self.warning=0
        elif self.come_back=="warning" :
            motors.state="warning"#stop the motors
            self.state="warning"
            self.warning+=1
        if self.come_back=="change":#if because we call change in nothing
            self.warning=0#restart the warning
            motors.state="warning"#stop the motors
            self.state="think"
            self.goal=goal=main_think(self.buoy_available,self.objectif,self.x,self.y,self.alpha)
        
        
    def warning(self) :
        if self.warning==1 :
            if self.wchck==0 :
                self.warning_time=temps.time()
                self.wchck=1
            else :
                if temps.time()-self.warning_time>2 :
                    self.state="check"
                    self.wchck=0
        else :#2 check
            self.warning=0
            self.get_out()
            
        
        
    def control(self) :
        global drop_brain,grab_brain

        if self.goal.history[0][3]=="point" :
            self.state=="strategy"
        if grab_brain.state=="un_active" :
            if self.goal.history[0][3]=="buoy":
                grab_brain.order="grab"
                #define all you need
                self.state=="strategy"
            elif self.goal.history[0][3]=="drop" :
                if self.chck==0 :
                    drop_brain.order="drop"
                    #define all you need
                    self.chck=1
                else :
                    if drop_brain.state=="un_active" :
                        self.chck=0
                        self.state=="strategy"
                        
                
        
    def move(self):
        if motors.state=="un_active" :
            self.state="think"
            self.goal=goal=main_think(self.buoy_available,self.objectif,self.x,self.y,self.alpha)


    def get_out(self) :#hide state
        xc,yc=self.the_issue_x,self.the_issue_y
        a,b=coef_b(self.x,self.y,self.goal.history[0][0],self.goal.history[0][1])
        global r_robot,r_opponant
        R=r_robot+e_opponant
        
        if a=="*" :#equation x=b
            A=1
            B=-2*yc
            C=yc**2-R**2+(b-xc)**2
            delta=B**2-4*A*C
            if delta==0 :#==> R=0
                y0=(-B)/(2*A)
                x0=b
                solution_x,solution_y,solution_alpha=x0,y0,self.alpha
    
            elif delta>0 :
                y1=(-B-math.sqrt(delta))/(2*A)
                y2=(-B+math.sqrt(delta))/(2*A)
                x1=b
                x2=b
                if distance_between_two_point(self.goal.history[0][0],self.goal.history[0][1],x1,y1)<distance_between_two_point(self.goal.history[0][0],self.goal.history[0][1],x2,y2) :#the opponant will be in front of us
                    alpha=angle_between_two_points(x1,y1,self.x,self.y)
                    solution_x,solution_y,solution_alpha=x1,y1,alpha
                else :
                    alpha=angle_between_two_points(x2,y2,self.x,self.y)
                    solution_x,solution_y,solution_alpha=x2,y2,alpha
        
        else:
            A=(1+a**2)
            B=2*(a*(b-yc)-xc)
            C=(xc**2+(b-yc)**2-R**2)
            delta=B**2-4*A*C
            if delta==0 :#==> R=0
                x0=(-B)/(2*A)
                y0=a*x0+b
                solution_x,solution_y,solution_alpha=x0,y0,self.alpha
            elif delta>0 :
                x1=(-B-math.sqrt(delta))/(2*A)
                x2=(-B+math.sqrt(delta))/(2*A)
                y1=a*x1+b
                y2=a*x2+b
                if distance_between_two_point(self.goal.history[0][0],self.goal.history[0][1],x1,y1)<distance_between_two_point(self.goal.history[0][0],self.goal.history[0][1],x2,y2) :#the opponant will be in front of us
                    alpha=angle_between_two_points(x1,y1,self.x,self.y)
                    solution_x,solution_y,solution_alpha=x1,y1,alpha
                else :
                    alpha=angle_between_two_points(x2,y2,self.x,self.y)
                    solution_x,solution_y,solution_alpha=x2,y2,alpha
        
        if respect_constraints(solution_x,solution_y) :
            motors.command(self.x,self.y,self.alpha,solution_x,solution_y,solution_alpha)
            self.state="move"
        else :
            self.state="check"
            
        
   
            
            