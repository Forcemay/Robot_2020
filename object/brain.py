import math
#Robot parameters :
green_capacity=3
red_capacity=3
distance_to_reach_the_buoy=187
cost_of_rotation_degree,cost_of_line_mm=0.0075,0.002
buoy_r=72/2
time_sort=0
time_constraint=95
drop_x=1800
drop_y=-1600
drop_alpha=270
r_robot=289/2
circle_security=10
r_robot=r_robot+circle_security
limit_history_obstacles=6#to avoid infinite loop for non reachable element, even though, the tangent function will bug before ^^, and I let it like this it's a good warning.
Weighted_A=5

###extract
def extract_buoy_available(buoy_available):#extract_buoy_available the bouy to define the paramaters in the object
    value_of_the_list=0
    for point in buoy_available :
        buoy_available[value_of_the_list]=buoy(point[0],point[1],point[2],"Initial")
        value_of_the_list+=1
###END extract
### For collision
class A_star_node() :
     def __init__(self,x,y,cost,heuristic,history) :
        global Weighted_A
        self.x=x
        self.y=y
        self.cost=cost
        self.heuristic=heuristic*Weighted_A #WA*
        self.history=history
            
    
def heuristic_object(a) :
    return a.heuristic
    
    
    
def sort_list_object(list,list_goal) :
    list.sort(key=heuristic_object)
    for node in list :
        if node.heuristic>list_goal[0].cost:
            list.remove(node)


    return list
    
def respect_constraints(x,y) :
    global r_robot
    respect=True
    if x<0 or x>3000 or y>0 or y<-2000 :
        respect=False
        return respect
    for j in range(len(circle)):#go through all the circle constraints
        a=circle[j].x
        b=circle[j].y
        r=circle[j].r+r_robot
        if (x-a)**2+(y-b)**2<r**2: #if in the constraints area
            respect=False
            return respect
    for i in range(len(rectangle)) :#go through all the rectangle constraints
        list_points=rectangle[i].list_points
        if list_points[0][0]-r_robot-4<x<list_points[3][0]+r_robot+4 :#if in x constraint +0.2 -0.2 see word
            
            if list_points[0][1]-r_robot-4<y<list_points[1][1]+r_robot+4 :#if in y constraint
                respect=False
                return respect
    return respect
    
def respect_constraints_info(x,y) :
    global r_robot
    respect=True
    if x<0 or x>3000 or y>0 or y<-2000 :
        return "%"
    for j in range(len(circle)):#go through all the circle constraints
        a=circle[j].x
        b=circle[j].y
        r=circle[j].r+r_robot
        if (x-a)**2+(y-b)**2<r**2: #if in the constraints area
            return str("c")+str(j)
    for i in range(len(rectangle)) :#go through all the rectangle constraints
        list_points=rectangle[i].list_points
        if list_points[0][0]-r_robot-4<x<list_points[3][0]+r_robot+4 :#if in x constraint +0.2 -0.2 see word
            
            if list_points[0][1]-r_robot-4<y<list_points[1][1]+r_robot+4 :#if in y constraint
                return str("r")+str(i)
    return respect
    
def in_list_po_high_cost(next_node,list_possibility):
    if len(list_possibility)!=0:
        for node in reversed(range(len(list_possibility))) :
            if list_possibility[node].x==next_node.x and list_possibility[node].y==next_node.y:
                if list_possibility[node].cost>=next_node.cost :#if in and cost higher
                    list_possibility.pop(node)#we find a better path to this point
                    return True,list_possibility#it's a new one
                else :
                    return False,list_possibility#it's a new one
                    
        return True,list_possibility#it's a new one
    else :
        return True,list_possibility
    

def the_path_through_osbstacles(node0,node_end,node_goal_impossible) :
    global limit_history_obstacles
    list_possibility=[node0]
    list_already_check=[]
    list_goal=[node_goal_impossible]
    while len(list_possibility)!=0 :
        current_node=list_possibility[0]#we take the latest
        list_possibility.pop(0) #supp
        if current_node.x==node_end.x and current_node.y==node_end.y and list_goal[0].cost>current_node.cost:
            list_goal=[]
            list_goal.append(current_node)
        else :
            for next_node in next_step(current_node,node_end) :
                the_best,list_possibility=in_list_po_high_cost(next_node,list_possibility)
                if the_best and respect_constraints(next_node.x,next_node.y) and len(next_node.history)<limit_history_obstacles:#<10 for the non reachable end point
                    if next_node.heuristic<list_goal[0].cost :#if the actual goal is not faster than the next one
                        list_possibility.append(next_node)
        list_already_check.append(current_node)
        list_possibility=sort_list_object(list_possibility,list_goal)#we look at the fastest first
    return list_goal



class circle_obstacles() :
    def __init__(self,x,y,r) :
        self.x=x
        self.y=y
        self.r=r
    
    
    def collision(self,x,y,x2,y2):
        #the infos which are gonna change
        Collision_info=False
        pointx=0
        pointy=0
        global r_robot
        #the line between the points
        coef,b=coef_b(x,y,x2,y2)
        d_constraint=r_robot+self.r
        
        interx,intery=projection_point(self.x,self.y,coef,b)

        if distance_between_two_point(x,y,interx,intery)>distance_between_two_point(x,y,x2,y2) :#if after the end point
            d=distance_between_two_point(x2,y2,self.x,self.y)
        else :
            if coef!="*" :
                d=distance_between_line_and_point(coef,-1,b,self.x,self.y)
            else :
                d=distance_between_line_and_point(-1,0,b,self.x,self.y)
        if d+0.01<d_constraint and projection_in(x,y,interx,intery,x2,y2,self.r,r_robot):#if you are to close (it goes through the circle),+0.01 for the tangent point
                Collision_info=True
                return Collision_info,[interx,intery]

        
        return Collision_info
            
    
    def bypass(self,x0,y0,x2,y2):
        #the 4 tangents
        global r_robot
        coef_tg1,coef_tg2,rest_tg1,rest_tg2=tangent(x0,y0,self.x,self.y,self.r+r_robot-0.01)#because we allowed before 0.01
        
        coef_tg12,coef_tg22,rest_tg12,rest_tg22=tangent(x2,y2,self.x,self.y,self.r+r_robot-0.01)
        #now the equality with the case equation x=a
        if coef_tg1==coef_tg12 or coef_tg2==coef_tg22 :
            return ["%","%"],["%","%"]
        else :
            if coef_tg1!="*" :
                if coef_tg12!="*" :#happen most of the time
                    new_x=(rest_tg1-rest_tg12)/(coef_tg12-coef_tg1)
                    new_y=coef_tg1*new_x+rest_tg1
                else :
                    new_x=rest_tg12 #equation x=x0
                    new_y=coef_tg1*new_x+rest_tg1
            else :#no coef_tg1=="*"==coeftg12
                new_x=rest_tg1 #equation x=x0
                new_y=coef_tg12*new_x+rest_tg12
            
            if coef_tg2!="*" :
                if coef_tg22!="*" :#happen most of the time
                    new_x2=(rest_tg2-rest_tg22)/(coef_tg22-coef_tg2)
                    new_y2=coef_tg2*new_x2+rest_tg2
                else :
                    new_x2=rest_tg22 #equation x=x0
                    new_y2=coef_tg2*new_x2+rest_tg2
            else :#no coef_tg1=="*"==coeftg12 impossible
                new_x2=rest_tg2 #equation x=x0
                new_y2=coef_tg22*new_x2+rest_tg22  
            
            return [new_x,new_y],[new_x2,new_y2]
class rectangle_obstacles():
    def __init__(self,x,y,l,L,x_c,y_c,x_c2,y_c2,r,r2) :#circle see word
        coef1,b1=coef_b(x,y,x,y+l)
        coef2,b2=coef_b(x+L,y+l,x+L,y)
        coef3,b3=coef_b(x,y,x+L,y)
        coef4,b4=coef_b(x,y+l,x+L,y+l)
        self.list_equation=[[coef1,b1],[coef2,b2],[coef3,b3],[coef4,b4]]
        self.list_points=[[x,y],[x,y+l],[x+L,y+l],[x+L,y]]
        #the center of the circle see word
        self.x_c=x_c
        self.y_c=y_c
        self.x_c2=x_c2
        self.y_c2=y_c2
        self.r=r
        self.r2=r2
        
    def collision(self,x,y,x2,y2):
        global r_robot
        coef,b=coef_b(x,y,x2,y2)
        Collision_info=False
        d_constraint=r_robot+self.r
        
        interx,intery=projection_point(self.x_c,self.y_c,coef,b)
        if distance_between_two_point(x,y,interx,intery)>distance_between_two_point(x,y,x2,y2) :#if after the end point
            d=distance_between_two_point(x2,y2,self.x_c2,self.y_c2)
        else :
            if coef!="*" :
                d=distance_between_line_and_point(coef,-1,b,self.x_c,self.y_c)
            else :
                d=distance_between_line_and_point(-1,0,b,self.x_c,self.y_c)
        
        if d+0.01<d_constraint and projection_in(x,y,interx,intery,x2,y2,self.r,r_robot):#if you are to close (it goes through the circle),0.01 for the tangent point
                Collision_info=True
                return Collision_info,[interx,intery]
                
        
        interx,intery=projection_point(self.x_c2,self.y_c2,coef,b)
        if distance_between_two_point(x,y,interx,intery)>distance_between_two_point(x,y,x2,y2) :#if after the end point
            d=distance_between_two_point(x2,y2,self.x_c2,self.y_c2)
        else :
            if coef!="*" :
                d=distance_between_line_and_point(coef,-1,b,self.x_c2,self.y_c2)
            else :
                d=distance_between_line_and_point(-1,0,b,self.x_c2,self.y_c2)
        if d+0.01<d_constraint and projection_in(x,y,interx,intery,x2,y2,self.r2,r_robot):#if you are to close (it goes through the circle),0.01 for the tangent point
                Collision_info=True
                return Collision_info,[interx,intery]
        
        if Collision_info==False :#check of the second condition
            for equation in self.list_equation:
                if intersection_2_line(coef,b,equation[0],equation[1])!=False :
                    pointx,pointy=intersection_2_line(coef,b,equation[0],equation[1])#the points of the intersection between one the equation and our path
                    if distance_between_two_point(pointx,pointy,x,y)+distance_between_two_point(pointx,pointy,x2,y2)>distance_between_two_point(x,y,x2,y2) :#if out (there is still a possibility of contact
                        pointx,pointy=closest_point(pointx,pointy,[[x,y],[x2,y2]])#but the point him cannot go further
                    if projection_in(x,y,pointx,pointy,x2,y2,0,r_robot) :
                        if crossed_circle_line(equation[0],equation[1],pointx,pointy,r_robot,self.list_points):#if there is a contact between the line and the circle and it's inside the constraint area, see word
                            Collision_info=True
                            return Collision_info,[pointx,pointy]
                            
        return Collision_info

    def bypass_c(self,x0,y0,x2,y2):
        global r_robot
        #the 4 tangents
        
        coef_tg1,coef_tg2,rest_tg1,rest_tg2=tangent(x0,y0,self.x_c,self.y_c,self.r+r_robot-0.01)
        
        coef_tg12,coef_tg22,rest_tg12,rest_tg22=tangent(x2,y2,self.x_c,self.y_c,self.r+r_robot-0.01)
        
        #now the equality with the case equation x=a
        if coef_tg1==coef_tg12 or +coef_tg2==coef_tg22 :
            return ["%","%"]
        else :
            if coef_tg1!="*" :
                if coef_tg12!="*" :#happen most of the time
                    new_x=(rest_tg1-rest_tg12)/(coef_tg12-coef_tg1)
                    new_y=coef_tg1*new_x+rest_tg1
                else :
                    new_x=rest_tg12 #equation x=x0
                    new_y=coef_tg1*new_x+rest_tg1
            else :#no coef_tg1=="*"==coeftg12
                new_x=rest_tg1 #equation x=x0
                new_y=coef_tg12*new_x+rest_tg12
            
            if coef_tg2!="*" :
                if coef_tg22!="*" :#happen most of the time
                    new_x2=(rest_tg2-rest_tg22)/(coef_tg22-coef_tg2)
                    new_y2=coef_tg2*new_x2+rest_tg2
                else :
                    new_x2=rest_tg22 #equation x=x0
                    new_y2=coef_tg2*new_x2+rest_tg2
            else :#no coef_tg1=="*"==coeftg12 impossible
                new_x2=rest_tg2 #equation x=x0
                new_y2=coef_tg22*new_x2+rest_tg22 
            d1=distance_between_two_point(self.x_c,self.y_c,new_x,new_y)+distance_between_two_point(self.x_c2,self.y_c2,new_x,new_y)
            d2=distance_between_two_point(self.x_c,self.y_c,new_x2,new_y2)+distance_between_two_point(self.x_c2,self.y_c2,new_x2,new_y2)
            if d1>=d2 :#we remove the one in the constraint because one is out one is in the constraint
                return [new_x,(new_y)]
            else :
                return [new_x2,new_y2]

    
    def bypass_c2(self,x0,y0,x2,y2):
        global r_robot
        #the 4 tangents
        coef_tg1,coef_tg2,rest_tg1,rest_tg2=tangent(x0,y0,self.x_c2,self.y_c2,self.r2+r_robot-0.01)
        
        coef_tg12,coef_tg22,rest_tg12,rest_tg22=tangent(x2,y2,self.x_c2,self.y_c2,self.r2+r_robot-0.01)
        if coef_tg1==coef_tg12 or coef_tg2==coef_tg22 :
            return ["%","%"]
        else :
            #now the equality with the case equation x=a
            if coef_tg1!="*" :
                if coef_tg12!="*" :#happen most of the time
                    new_x=(rest_tg1-rest_tg12)/(coef_tg12-coef_tg1)
                    new_y=coef_tg1*new_x+rest_tg1
                else :
                    new_x=rest_tg12 #equation x=x0
                    new_y=coef_tg1*new_x+rest_tg1
            else :#no coef_tg1=="*"==coeftg12
                new_x=rest_tg1 #equation x=x0
                new_y=coef_tg12*new_x+rest_tg12
            
            if coef_tg2!="*" :
                if coef_tg22!="*" :#happen most of the time
                    new_x2=(rest_tg2-rest_tg22)/(coef_tg22-coef_tg2)
                    new_y2=coef_tg2*new_x2+rest_tg2
                else :
                    new_x2=rest_tg22 #equation x=x0
                    new_y2=coef_tg2*new_x2+rest_tg2
            else :#no coef_tg1=="*"==coeftg12 impossible
                new_x2=rest_tg2 #equation x=x0
                new_y2=coef_tg22*new_x2+rest_tg22 
            
            d1=distance_between_two_point(self.x_c,self.y_c,new_x,new_y)+distance_between_two_point(self.x_c2,self.y_c2,new_x,new_y)
            d2=distance_between_two_point(self.x_c,self.y_c,new_x2,new_y2)+distance_between_two_point(self.x_c2,self.y_c2,new_x2,new_y2)
            if d1>=d2 :#we remove the one in the constraint because one is out one is in the constraint
                return [new_x,(new_y)]
            else :
                return [new_x2,new_y2]



###FOR the collision
def projection_point(x,y,coef,b):
    if coef=="*":#x=b
        coef2=0
        b2=y
        interx,intery=intersection_2_line(coef,b,coef2,b2)#cannot be false
        
        
    else :
        if coef==0 : #y=b
            coef2="*"
            b2=x
            interx,intery=intersection_2_line(coef,b,coef2,b2)#cannot be false
        else :
            coef2=-1/coef
            b2=y-coef2*x
            interx,intery=intersection_2_line(coef,b,coef2,b2)#cannot be false
            
    return interx,intery

def projection_in(x,y,x1,y1,x2,y2,r1,r2):#the Start point the new one, the end, the constraint of the point and the constraint of the robot
    if distance_between_two_point(x,y,x1,y1)+distance_between_two_point(x1,y1,x2,y2)<distance_between_two_point(x,y,x2,y2)+2*(r1+r2):
        return True
    else :
        return False
    

def inside_constraint_area(x,y,list_points,coef,b):
    point1x=-9999
    point1y=-9999
    point2x=-9999
    point2y=-9999
    for point in list_points :
        if coef=="*" :
            if point[0]==b :#if y=b
                if point1x==-9999 :#if it'is the first point
                    point1x=point[0]
                    point1y=point[1]#we register the point
                else :
                    point2x=point[0]
                    point2y=point[1]#no more than two points in a not curve surface, otherwise you have to register the points manually
                    break
        
        else :
            if point[0]*coef+b==point[1]:#if the point is on the line, that means, no curve surface
                if point1x==-9999 :#if it'is the first point
                    point1x=point[0]
                    point1y=point[1]#we register the point
                else :
                    point2x=point[0]
                    point2y=point[1]#no more than two points in a not curve surface, otherwise you have to register the points manually
                    break
                    
    if distance_between_two_point(x,y,point1x,point1y)+distance_between_two_point(x,y,point2x,point2y)==distance_between_two_point(point2x,point2y,point1x,point1y): #|AB|+|BC|=|AC|
        
        return True
    else :
        
        return False
                
                


def crossed_circle_line(a,b,xc,yc,R,list_points):#ax+b (x-xc)**2+(y-yc)**2=R**2
    if a=="*" :#equation x=b
        A=1
        B=-2*yc
        C=yc**2-R**2+(b-xc)**2
        delta=B**2-4*A*C
        if delta==0 :#==> R=0
            y0=(-B)/(2*A)
            x0=b
            if inside_constraint_area(x0,y0,list_points,a,b) :
                return True
            else:
                return False
        elif delta>0 :
            y1=(-B-math.sqrt(delta))/(2*A)
            y2=(-B+math.sqrt(delta))/(2*A)
            x1=b
            x2=b
            if inside_constraint_area(x1,y1,list_points,a,b) or inside_constraint_area(x2,y2,list_points,a,b) :
                return True
            else :
                return False
        else :#impossible
            return False
    
    else:
        A=(1+a**2)
        B=2*(a*(b-yc)-xc)
        C=(xc**2+(b-yc)**2-R**2)
        delta=B**2-4*A*C
        if delta==0 :#==> R=0
            x0=(-B)/(2*A)
            y0=a*x0+b
            if inside_constraint_area(x0,y0,list_points,a,b) :
                return True
            else:
                return False
        elif delta>0 :
            x1=(-B-math.sqrt(delta))/(2*A)
            x2=(-B+math.sqrt(delta))/(2*A)
            y1=a*x1+b
            y2=a*x2+b
            if inside_constraint_area(x1,y1,list_points,a,b) or inside_constraint_area(x2,y2,list_points,a,b) :
                return True
            else :
                return False
        else :#impossible
            return False
        
        

def coef_b(x,y,x2,y2) :
    if x==x2 :
        coef="*"
        b=x
    else:
        coef=(y2-y)/(x2-x)
        b=y-coef*x
    return coef,b
def intersection_2_line(a,b,a2,b2): 
    
    if a==a2 :
        return False
    
    elif a=="*" :
        x=b
        y=a2*x+b2
        return x,y
        
    elif a2=="*" :
        x=b2
        y=a*x+b
        return x,y
    else :

        x=(b2-b)/(a-a2)
        y=a*x+b
        return x,y
def closest_point(x,y,list):
    distance_min=999999999
    for p in list :

        d=distance_between_two_point(x,y,p[0],p[1])
        if d<distance_min :
            pointx=p[0]
            pointy=p[1]
            distance_min=d
    if len(list)==0 :#if no point
        pointx=x
        pointy=y
    return pointx,pointy    
def distance_between_line_and_point(A,B,C,x,y) :#https://lexique.netmath.ca/distance-entre-un-point-et-une-droite/
    distance=abs((A*x+B*y+C)/(math.sqrt(A**2+B**2)))
    return distance
def distance_between_two_point(x,y,x2,y2):
    return math.sqrt((y2-y)**2+(x-x2)**2)
    
    
def intersection_2_circle(x_c,y_c,x_c2,y_c2,r,R):#for the point the grab the buoy in case of a non reachable solution for the straight line, see word.
    Xa,Ya,Xb,Yb,r,R=x_c,y_c,x_c2,y_c2,r,R
    a=2*(Xb-Xa)
    b=2*(Yb-Ya)
    c=(Xb-Xa)**2+(Yb-Ya)**2-R**2+r**2
    delta=(2*a*c)**2-4*(a**2+b**2)*(c**2-(b**2)*r**2)
    if delta>=0 :
        Xp=Xa+(2*a*c-math.sqrt(delta))/(2*(a**2+b**2))
        Xq=Xa+(2*a*c+math.sqrt(delta))/(2*(a**2+b**2))
        if b==0 :
            if R**2-((2*c-a**2)/(2*a))**2>=0 :
                Yp=Ya+(b/2)+math.sqrt(R**2-((2*c-a**2)/(2*a))**2)
                Yq=Ya+(b/2)-math.sqrt(R**2-((2*c-a**2)/(2*a))**2)
            else :
                return False,False,False,False
        else :
            Yp=Ya+(c-a*(Xp-Xa))/b
            Yq=Ya+(c-a*(Xq-Xa))/b
        return Xp,Yp,Xq,Yq
    else :
        return False,False,False,False

def tangent(x0,y0,x,y,r):
        #see the word with the circle  https://members.loria.fr/Roegel/loc/note0001.pdf
    #part two circlesn note : there is always 2 solutions one solution is not possible (2 tangents)
    Xa,Ya,Xb,Yb,R=x,y,(x+x0)/2,(y+y0)/2,distance_between_two_point(x,y,x0,y0)/2
    a=2*(Xb-Xa)
    b=2*(Yb-Ya)
    c=(Xb-Xa)**2+(Yb-Ya)**2-R**2+r**2
    delta=(2*a*c)**2-4*(a**2+b**2)*(c**2-(b**2)*r**2)
    if delta<0:
        print("bug",x0,y0,x,y,r)
    Xp=Xa+(2*a*c-math.sqrt(delta))/(2*(a**2+b**2))
    Xq=Xa+(2*a*c+math.sqrt(delta))/(2*(a**2+b**2))
    if b==0 :
        Yp=Ya+(b/2)+math.sqrt(R**2-((2*c-a**2)/(2*a))**2)
        Yq=Ya+(b/2)-math.sqrt(R**2-((2*c-a**2)/(2*a))**2)
    else :
        Yp=Ya+(c-a*(Xp-Xa))/b
        Yq=Ya+(c-a*(Xq-Xa))/b
        
    #now we are going to set up the equation of the tangent
    if Xp!=x0 :
        coef_tg1=(Yp-y0)/(Xp-x0)
        rest_tg1=y0-coef_tg1*x0

    else :
        coef_tg1="*"
        rest_tg1=x0
    if Xq!=x0:
        coef_tg2=(Yq-y0)/(Xq-x0)
        rest_tg2=y0-coef_tg2*x0
    else :
        coef_tg2="*"
        rest_tg2=x0
    return coef_tg1,coef_tg2,rest_tg1,rest_tg2
    



                
                
            
        
def issues(x,y,x2,y2) :
    global rectangle,circle
    list_obstacle_points=[]
    for j in range(len(circle)):#go through all the circle constraints
        if circle[j].collision(x,y,x2,y2)!=False :
            return True
            
    for i in range(len(rectangle)) :#go through all the rectangle constraints
        if rectangle[i].collision(x,y,x2,y2)!=False :
            return True
            
    return False

def round_trip(node):#check the round trip
    for point in node.history :
        if node.x-0.01<point[0]<node.x+0.01 and node.y-0.01<point[1]<node.y+0.01:
            return True
    return False
    
def smooth(node,node_end) :#smooth the path
    history=[]#we take only the history because the last point have to respect a constraint, all the time
    for point in node.history :
        history.append(point)
    length=len(history)
    value=0
    while value<len(history)-1 :#we don't to check the last node with himself
        for point in reversed(range(value+1,len(history))):#don't want to check value with himself
            if issues(history[value][0],history[value][1],history[point][0],history[point][1])==False :
                history=history[:value+1]+history[point:]
                break
        value+=1
    if length!=len(history) :#if we have changed the history
        cost=0
        for point in range(len(history)-1):
            cost=cost+distance_between_two_point(history[point][0],history[point][1],history[point+1][0],history[point+1][1])
        cost=cost+distance_between_two_point(history[-1][0],history[-1][1],node.x,node.y)
        heuristic=cost+distance_between_two_point(node.x,node.y,node_end.x,node_end.y)
        node.history=history
        node.cost=cost
        node.heuristic=heuristic
    
    return node
    
def next_step(node,node_end):
    obstacle=issues(node.x,node.y,node_end.x,node_end.y)
    history=[]
    list_new_nodes=[]
    for x in node.history :
        history.append(x)
    history.append([node.x,node.y])
    if obstacle==False:
        cost=node.cost+distance_between_two_point(node_end.x,node_end.y,node.x,node.y)
        end_node=A_star_node(node_end.x,node_end.y,cost,cost,history)
        list=[end_node]
        return list
    else :#if there is a obstacle
        for j in range(len(circle)):#go through all the circle constraints
            bypass_0=circle[j].bypass(node.x,node.y,node_end.x,node_end.y)
            bypass_1=bypass_0[0]
            bypass_2=bypass_0[1]
            if bypass_1[0]!="%" :#case straight line by bypass tg1=tg2
                cost1=node.cost+distance_between_two_point(node.x,node.y,bypass_1[0],bypass_1[1])#we neglect the rotation because we don't know in which direction it will point
                heuristic1=distance_between_two_point(node_end.x,node_end.y,bypass_1[0],bypass_1[1])
                cost2=node.cost+distance_between_two_point(node.x,node.y,bypass_2[0],bypass_2[1])
                heuristic2=distance_between_two_point(node_end.x,node_end.y,bypass_2[0],bypass_2[1])
                
                bypass_1=A_star_node(bypass_1[0],bypass_1[1],cost1,cost1+heuristic1,history)
                bypass_2=A_star_node(bypass_2[0],bypass_2[1],cost2,cost2+heuristic2,history)
                if issues(node.x,node.y,bypass_1.x,bypass_1.y)==False and round_trip(bypass_1)==False:#if we can go to this point
                    list_new_nodes.append(bypass_1)
                if issues(node.x,node.y,bypass_2.x,bypass_2.y)==False and round_trip(bypass_2)==False:
                    list_new_nodes.append(bypass_2)

                
        for i in range(len(rectangle)) :#go through all the rectangle constraints
            bypass_1=rectangle[i].bypass_c(node.x,node.y,node_end.x,node_end.y)
            bypass_2=rectangle[i].bypass_c2(node.x,node.y,node_end.x,node_end.y)
            if bypass_1[0]!="%" and bypass_2[0]!="%":
                cost1=node.cost+distance_between_two_point(node.x,node.y,bypass_1[0],bypass_1[1])#we neglect the rotation because we don't know in which direction it will point
                heuristic1=distance_between_two_point(node_end.x,node_end.y,bypass_1[0],bypass_1[1])
                cost2=node.cost+distance_between_two_point(node.x,node.y,bypass_2[0],bypass_2[1])
                heuristic2=distance_between_two_point(node_end.x,node_end.y,bypass_2[0],bypass_2[1])
                
                bypass_1=A_star_node(bypass_1[0],bypass_1[1],cost1,cost1+heuristic1,history)
                bypass_2=A_star_node(bypass_2[0],bypass_2[1],cost2,cost2+heuristic2,history)
                if issues(node.x,node.y,bypass_1.x,bypass_1.y)==False and round_trip(bypass_1)==False:#if we can go to this point
                    list_new_nodes.append(bypass_1)
                if issues(node.x,node.y,bypass_2.x,bypass_2.y)==False and round_trip(bypass_2)==False:
                    list_new_nodes.append(bypass_2)
    

                    
                                
            
        

        return list_new_nodes
    
###END collision

###A_star
class buoy():
    def __init__(self, color, x,y,state):
        self.color = color
        self.x = x
        self.y = y
        self.position=0#position for the storage
        self.state=state
    
    def Drop(self,x,y) :
        self.x=x
        self.y=y
        self.state="Placed"
    
    def Grab(self,position) :
        self.x=-2
        self.y=-2
        self.position=position
        self.state="stocked"
class A_star_node_main() :
     def __init__(self,pointx,pointy,alpha,x_real,y_real,history,history_real,green,red,cost,cost_heurisitc,time) :
        self.x=pointx
        self.y=pointy
        self.alpha=alpha
        self.x_real=x_real
        self.y_real=y_real
        self.history=history
        self.history_real=history_real
        self.red=red
        self.green=green
        self.cost=cost
        self.heuristic=cost_heurisitc
        self.time=time#time of the actual point in the reality
def operation_to_reach(x1,y1,alpha1,x2,y2,alpha2):#what to do ? same code as last year YESS less to do \o/ and this time we don't have to take into account the reverse gear manually that's done by the code.
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
    
    
def cost_do_movement(rot1,distance,rot2) :#all the three operations to do a straight line, the first rotation to be in the good direction, the distance to browse and finally you need to handle the last rotation
    global cost_of_rotation_degree,cost_of_line_mm
    cost_movement=(abs(rot1)+abs(rot2))*cost_of_rotation_degree+abs(distance)*cost_of_line_mm
    return cost_movement
    
def coef_b(x,y,x2,y2) :
    if x==x2 :
        coef="*"
        b=x
    else:
        coef=(y2-y)/(x2-x)
        b=y-coef*x
    return coef,b
def distance_between_two_point(x,y,x2,y2):
    return math.sqrt((y2-y)**2+(x-x2)**2)
    
def crossed_circle_line_position(x,y,xc,yc):#ax+b (x-xc)**2+(y-yc)**2=R**2
    global distance_to_reach_the_buoy
    R=distance_to_reach_the_buoy
    a,b=coef_b(x,y,xc,yc)
    
    if a=="*" :#equation x=b
        A=1
        B=-2*yc
        C=yc**2-R**2+(b-xc)**2
        delta=B**2-4*A*C
        if delta==0 :#==> R=0
            y0=(-B)/(2*A)
            x0=b
            return x0,y0

        elif delta>0 :
            y1=(-B-math.sqrt(delta))/(2*A)
            y2=(-B+math.sqrt(delta))/(2*A)
            x1=b
            x2=b
            if distance_between_two_point(x,y,x1,y1)<distance_between_two_point(x,y,x2,y2) :
                alpha=angle_between_two_points(x,y,x1,y1)
                return x1,y1,alpha
            else :
                alpha=angle_between_two_points(x,y,x2,y2)#same but ^^
                return x2,y2,alpha
    
    else:
        A=(1+a**2)
        B=2*(a*(b-yc)-xc)
        C=(xc**2+(b-yc)**2-R**2)
        delta=B**2-4*A*C
        if delta==0 :#==> R=0
            x0=(-B)/(2*A)
            y0=a*x0+b
            return x0,y0
        elif delta>0 :
            x1=(-B-math.sqrt(delta))/(2*A)
            x2=(-B+math.sqrt(delta))/(2*A)
            y1=a*x1+b
            y2=a*x2+b
            if distance_between_two_point(x,y,x1,y1)<distance_between_two_point(x,y,x2,y2) :
                alpha=angle_between_two_points(x,y,x1,y1)
                return x1,y1,alpha
            else :
                alpha=angle_between_two_points(x,y,x2,y2)
                return x2,y2,alpha
        else :#impossible
            return False    
def heuristic_object(a) :
    return a.heuristic
    
def angle_between_two_points(x,y,x2,y2):#return the angle between 2 points and x
    if y2>y :
        angle=math.atan2(y2-y,x2-x)*180/math.pi
        
    elif y>y2 :
        angle=360+math.atan2(y2-y,x2-x)*180/math.pi
    
    else:#y=y2
        if x>x2:
            angle=180
        else :
            angle=0
            
    return angle    
    
def sort_list_object(list,list_goal) :
    list.sort(key=heuristic_object)
    for node in list :
        if node.heuristic>list_goal[0].cost:
            list.remove(node)


    return list
    


def new(buoy_available,history_real,objectif) :
    new_buoy=[]
    avoid=[]
    for node in buoy_available :
        if [node.x,node.y] not in history_real :
            if [node.color,node.x,node.y] in objectif:
                new_buoy.append(node)
            avoid.append(node)
    return new_buoy,avoid

def closest(pointx,pointy,list_node) :
    list=[]
    for node in list_node :
        if node.x!=pointx and node.y!=pointy :
            list.append([node.x,node.y])
            
    closestx,closesty=closest_point(pointx,pointy,list)
    return closestx,closesty
    
def respect_constraints_time(node) :
    respect=True
    global r_robot,time_constraint,time_sort,drop_x,drop_y,drop_alpha
    rot1,distance,rot2=operation_to_reach(node.x,node.y,node.alpha,drop_x,drop_y,drop_alpha)
    cost=node.time+node.cost+cost_do_movement(rot1,distance,rot2)+time_sort
    if cost>time_constraint:
        respect=False
        return respect
    return respect

        
    
def next_step_main(node,objectif) :
    global green_capacity,red_capacity,circle,buoy_r,distance_to_reach_the_buoy
    list=[]
    
    history_real=[]
    for m in node.history_real :
        history_real.append(m)
    history_real.append([node.x_real,node.y_real])    
    ct=0
    new_buoy_available,avoid_list=new(buoy_available,history_real,objectif)
    lenght=len(circle)
    for next_node in new_buoy_available :
        #we re-define history and history_real each time to unlink the list 
        history=[]
        for i in node.history :
            history.append(i)
    
        history.append([node.x,node.y,node.alpha])
    
        history_real=[]
        for m in node.history_real :
            history_real.append(m)
        history_real.append([node.x_real,node.y_real])

        pointx,pointy,alpha=crossed_circle_line_position(node.x,node.y,next_node.x,next_node.y)
        rot1,distance,rot2=operation_to_reach(node.x,node.y,node.alpha,pointx,pointy,alpha)
        cost=node.cost+cost_do_movement(rot1,distance,rot2)
        closestx,closesty=closest(next_node.x,next_node.y,new_buoy_available)
        cost_heurisitc=cost+cost_do_movement(0,distance_between_two_point(pointx,pointy,closestx,closesty),0)
        for buoy in avoid_list :
            if buoy.x!=next_node.x or buoy.y!=next_node.y :
                circle.append(circle_obstacles(buoy.x,buoy.y,buoy_r))#define all the other buoys as obstacles (we don't want to move them)
        respect=respect_constraints_info(pointx,pointy)#check
        you_can=True
        if respect!=True :#lets try to make it reachable
            you_can=False
            if respect!="%" :#if not out (not done so far)
                if respect[0]=="r" :#rectangle
                    you_can=False

                else :#circle
                    x1,y1,x2,y2=intersection_2_circle(next_node.x,next_node.y,circle[int(respect[1])].x,circle[int(respect[1])].y,distance_to_reach_the_buoy,circle[int(respect[1])].r+r_robot)#return the two point which allow the grab given the constraint
                    if x1!=False: #if there is a solution
                        pointx,pointy=closest_point(pointx,pointy,[[x1,y1],[x2,y2]])
                        respect=respect_constraints_info(pointx,pointy)#check
                        if respect==True :
                            you_can=True
                    
        if you_can==True:#if the point is reachable
            if next_node.color=="green" :
                green=node.green+1
                red=node.red            
            else :
                red=node.red+1
                green=node.green
            if red<=red_capacity and green<=green_capacity:
                p=0
                p=update_obstacles(A_star_node_main(pointx,pointy,alpha,next_node.x,next_node.y,history,history_real,green,red,cost,cost_heurisitc,node.time))#define the node +changes it if necessary
                if p.x!="%" :#if the path is possible
                    list.append(ct)
                    list[ct]=p
                    ct+=1
        circle=circle[:lenght]#remove 
    return list
def A_search_main(node0,node_goal_impossible,objectif) :
    global green_capacity,red_capacity
    list_possibility=[node0]
    list_already_check=[]
    list_goal=[node_goal_impossible]
    survy=node_goal_impossible
    while len(list_possibility)!=0 :
        current_node=list_possibility[0]#we take the latest
        list_possibility.pop(0) #supp
        if current_node.green+current_node.red>=survy.green+survy.red:#we take the one with the most buoys.
            if current_node.green+current_node.red>survy.green+survy.red:#for the >
                survy=current_node
                
            else :#for the =
                if current_node.cost<survy.cost :#if faster
                    survy=current_node
        if current_node.green==green_capacity and current_node.red==red_capacity:
            if next_node.heuristic<list_goal[0].cost :
                list_goal=[]
                list_goal.append(current_node)
        
        else :
            for next_node in next_step_main(current_node,objectif) :
                if respect_constraints_time(next_node):#respect time constraints
                    if next_node.heuristic<list_goal[0].cost :#if the actual goal is not faster than the next one
                        list_possibility.append(next_node)
        list_already_check.append(current_node)
        list_possibility=sort_list_object(list_possibility,list_goal)#we look at the fastest first
    if list_goal[0]==node_goal_impossible :#if you no solution
        list_goal=[]
        list_goal.append(survy)
    
    return list_goal
    
def extract_constraints_area(circle,rectangle):
    value=0
    for p in circle:
        circle[value]=circle_obstacles(p[0],p[1],p[2])
        value+=1
    value=0
    for p in rectangle:
        rectangle[value]=rectangle_obstacles(p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9])
        value+=1
### END A_star

### FOR THE BYPASS
def update_obstacles(node) :#use A* to compute the best path through the obstacles.
    global time,drop_x2,drop_y2,drop_alpha2

    node0=A_star_node(node.history[-1][0],node.history[-1][1],0,0,[])
    node_end=A_star_node(node.x,node.y,0,0,[])
    
    node_goal_impossible=A_star_node("%","%",10000,10000,[])#the cost very high is the only think important
    new_path=the_path_through_osbstacles(node0,node_end,node_goal_impossible)
    if new_path[0].x=="%" :#there is no path
        node.x="%"
    elif len(new_path[0].history)>1 :#have to avoid an obstacle

        new_path[0]=smooth(new_path[0],node_end)
        length=len(node.history)
        time_previous=node.cost
        for x in range(1,len(new_path[0].history)): #we don't want to have twice the previous node.
            node.history.append(new_path[0].history[x]+[angle_between_two_points(new_path[0].history[x][0],new_path[0].history[x][1],new_path[0].history[x-1][0],new_path[0].history[x-1][1])])#add the new path in the history

        added_time=0
        for point in range(length-1,len(node.history)-1) :
            rot1,distance,rot2=operation_to_reach(node.history[point][0],node.history[point][1],node.history[point][2],node.history[point+1][0],node.history[point+1][1],node.history[point+1][2])
            
            added_time=added_time+cost_do_movement(rot1,distance,rot2)
            
        time_until_node=added_time+time_previous
        
        node.heuristic=node.heuristic-node.cost+time_until_node
        node.cost=time_until_node
    return node
                
### END BYPASS
def main_brain(circle,buoy_available,objectif,x0,y0,angle0) :             
    global rectangle
    extract_buoy_available(buoy_available)
    extract_constraints_area(circle,rectangle)
    node0=A_star_node_main(x0,y0,angle0,x0,y0,[],[],0,0,0,0,0)
    node_goal_impossible=A_star_node_main(x0,y0,angle0,x0,y0,[],[],0,0,999999,999999,0)

    goal=A_search_main(node0,node_goal_impossible,objectif)

    return goal
import time as temps
start_time = temps.time()

from random import randrange



rectangle=[[889,-2000,150,22,900,-1860,900,-1990,distance_between_two_point(900,-1990,889,-2000),distance_between_two_point(900,-1990,889,-2000)],[1489,-2000,300,22,1500,-1990,1500,-1710,distance_between_two_point(1489,-2000,1500,-1990),distance_between_two_point(1489,-2000,1500,-1990)],[2089,-2000,150,22,2100,-1990,2100,-1860,distance_between_two_point(900,-1990,889,-2000),distance_between_two_point(900,-1990,889,-2000)]]


buoy_available=[["red",1100,-800],["red",2050,-400],["red",1935,-1650],["red",1730,-1200],["red",1605,-1955],["red",1335,-1650],["red",1005,-1955],["red",670,-100],["red",450,-1080],["red",300,-400],["green",2330,-100],["green",1995,-1955],["green",1900,-800],["green",1665,-1650],["green",1395,-1955],["green",1270,-1200],["green",1065,-1650],["green",950,-400],["green",450,-510],["green",300,-1200]]
objectif=[["green",1270,-1200],["red",1730,-1200],["green",1900,-800],["red",2050,-400],["green",1665,-1650],["red",1935,-1650]]

for z in range(20) :
    p=randrange(0,3001)
    r=randrange(-2000,1)
    # p,r=876,-633
    print(p,r)
    circle=[[p,r,289/2]]
    buoy_available=[["red",1100,-800],["red",2050,-400],["red",1935,-1650],["red",1730,-1200],["red",1605,-1955],["red",1335,-1650],["red",1005,-1955],["red",670,-100],["red",450,-1080],["red",300,-400],["green",2330,-100],["green",1995,-1955],["green",1900,-800],["green",1665,-1650],["green",1395,-1955],["green",1270,-1200],["green",1065,-1650],["green",950,-400],["green",450,-510],["green",300,-1200]]
    objectif=[["green",1270,-1200],["red",1730,-1200],["green",1900,-800],["red",2050,-400],["green",1665,-1650],["red",1935,-1650]]
    rectangle=[[889,-2000,150,22,900,-1860,900,-1990,distance_between_two_point(900,-1990,889,-2000),distance_between_two_point(900,-1990,889,-2000)],[1489,-2000,300,22,1500,-1990,1500,-1710,distance_between_two_point(1489,-2000,1500,-1990),distance_between_two_point(1489,-2000,1500,-1990)],[2089,-2000,150,22,2100,-1990,2100,-1860,distance_between_two_point(900,-1990,889,-2000),distance_between_two_point(900,-1990,889,-2000)]]
    goal=main_brain(circle,buoy_available,objectif,1750,-250,0)
    
    
    
    
    
    print("Temps d execution : %s secondes ---" % (temps.time() - start_time))
    
    import numpy as np
    import matplotlib.pyplot as plt
    
    x_points=[]
    y_points=[]
    for x in goal[0].history:
        x_points.append(x[0])
        y_points.append(x[1])
    x_points.append(goal[0].x)
    y_points.append(goal[0].y)
        
    
    
    n=[]
    
    for x in range(len(x_points)):
        n.append(x)
    fig, ax = plt.subplots()
    ax.scatter(x_points, y_points)
    for i, txt in enumerate(n):
        ax.annotate(txt, (x_points[i], y_points[i]))
    for i in range(len(x_points)):
        plt.plot(x_points,y_points, 'ro-')
    for f in buoy_available :
        if f.color=="green":
            cl="g"
        else :
            cl="r"
        plt.plot(f.x,f.y,'ro-',color=cl)
    plt.title('The last hope')
    plt.xlabel('x')
    plt.ylabel('y')
    
    plt.savefig('ScatterPlot_01.png')
    
    
    circle1 = plt.Circle((p,r),289+10, color='r')
    
    
    
    
    rect = plt.Rectangle((889,-2000),22,150,linewidth=1,edgecolor='r',facecolor='none')
    rect2 = plt.Rectangle((1489,-2000),22,300,linewidth=1,edgecolor='r',facecolor='none')
    rect3 = plt.Rectangle((2089,-2000),22,150,linewidth=1,edgecolor='r',facecolor='none')
    
    ax.add_artist(circle1)
    
    ax.add_artist(rect)
    ax.add_artist(rect2)
    ax.add_artist(rect3)
    ax.set_aspect(1)
    
    
    
    plt.title('A*')
    plt.xlabel('x')
    plt.ylabel('y')
    
    plt.savefig('ScatterPlot_01.png')
    plt.show()
    
