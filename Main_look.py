rectangle_size=35
distance_to_remove_the_tower=30
position_tower_x=1500
position_tower_y=0
import time as temps
start=temps.time()
import pandas as pd
import numpy as np
import sklearn.metrics as sm
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import datasets
import math


import os
os.chdir("C:/Users/Mayeul/Documents/Projet_Robot_2020")

def distance_between_two_point(x,y,x2,y2):
    return math.sqrt((y2-y)**2+(x-x2)**2)
def center(x,y,x2,y2) :
    return (x+x2)/2,(y+y2)/2
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
        
def perpendicular(a,b,xc,yc) :
    if a==0:
        a_p="*"
        b_p=xc
    elif a=="*" :
        a_p=0
        b_p=yc
    else :
        a_p=-1/a
        b_p=yc-a_p*xc
    return a_p,b_p

def the_point_structure(list,position_x,position_y) :
    if len(list)>6 :
        list_x=[]
        list_y=[]
        list2_x=[]
        list2_y=[]
        for point in range(math.ceil(len(list)/3)) :
            list_x.append(list[point][0])
            list_y.append(list[point][1])
            list2_x.append(list[len(list)-1-point][0])
            list2_y.append(list[len(list)-1-point][1])
        fit = np.polyfit(list_x, list_y, 1)
        if math.isnan(fit[0]) :
            a="*"
            b=list_x[0]
        else :
            a=fit[0]
            b=fit[1]
        
        fit2 = np.polyfit(list2_x, list2_y, 1)
        if math.isnan(fit2[0]) :
            a2="*"
            b2=list_x[0]
        else :
            a2=fit2[0]
            b2=fit2[1]
        global rectangle_size
        if math.atan(abs((a2-a)/(1+a*a2)))*180/math.pi<15 :#if the angle between both lines is lower thatn 15°
            centerx,centery=center(list[0][0],list[0][1],list[-1][0],list[-1][1])
            a_p,b_p=perpendicular(a,b,centerx,centery)
            pointx,pointy=cercle_line_structure_farest(position_x,position_y,a_p,b_p,centerx,centery,rectangle_size)
        else :
            centerx,centery=intersection_2_line(a,b,a2,b2)#intersection two line
            x1,y1=cercle_line_structure_closest(list[0][0],list[0][1],a,b,centerx,centery,1)#the point for the middle line
            x2,y2=cercle_line_structure_closest(list[-1][0],list[-1][1],a2,b2,centerx,centery,1)#second one
            a1_p,b1_p=perpendicular(a,b,x1,y1)#the two coef
            a2_p,b2_p=perpendicular(a2,b2,x2,y2)
            u,v=intersection_2_line(a1_p,b1_p,a2_p,b2_p)
            a3_p,b3_p=coef_b(centerx,centery,u,v)#intersection of the new perpendicular
            pointx,pointy=cercle_line_structure_farest(position_x,position_y,a3_p,b3_p,centerx,centery,rectangle_size*math.sqrt(2))#the point
        return pointx,pointy
    
    else :
        centerx,centery=closest_point(position_x,position_y,list)
        c,b=coef_b(position_x,position_y,centerx,centery)
        pointx,pointy=cercle_line_structure_farest(position_x,position_y,c,b,centerx,centery,rectangle_size)
        return pointx,pointy
def cercle_line_structure_closest(x,y,a,b,xc,yc,r) :#ax+b (x-xc)**2+(y-yc)**2=R**2
    
    
    R=r
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
                return x1,y1
            else :
                return x2,y2
    
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
                return x1,y1
            else :
                return x2,y2
        else :#impossible
            return False    
def cercle_line_structure_farest(x,y,a,b,xc,yc,r) :#ax+b (x-xc)**2+(y-yc)**2=R**2
    
    
    R=r
    
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
            if distance_between_two_point(x,y,x1,y1)>distance_between_two_point(x,y,x2,y2) :
                return x1,y1
            else :
                return x2,y2
    
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
            if distance_between_two_point(x,y,x1,y1)>distance_between_two_point(x,y,x2,y2) :
                return x1,y1
            else :
                return x2,y2
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


def extract_filter(position_x,position_y) :
    mon_fichier = open("01.txt", "r")
    read=mon_fichier.read()
    list=[]
    list_inside=[]
    ct=0
    while ct!=len(read):
        if read[ct]!="\n" :
            list_inside.append(read[ct])
        else :
            list.append(list_inside)
            list_inside=[]
        ct+=1
    list.append(list_inside)
    list.pop(0)
    list.pop(0)
    list.pop(0)
    list2=[]
    list2_inside=[]
    for s in list :
        re=""
        for p in s :
            if p!=" ":
                re+=p
            
            else :
                list2_inside.append(float(re))
                re=""
        if len(re)!=0 :
            list2_inside.append(float(re))
        if len(list2_inside)!=0 :
            list2.append(list2_inside)
            list2_inside=[]
    list=[]
    
    #ok now we have only the distance and the angle with that we"re gonna creat a map with for origin our robot.
    for x in list2 :
        x.pop()
        u=int(position_x+x[1]*math.sin(x[0]*math.pi/180))
        v=int(position_y+x[1]*math.cos(x[0]*math.pi/180))
        if 0<u<3000 and -2000<v<0:#we supp everything outside the field
            list.append([u,v])
        
    return list
    



def main_look(position_x,position_y) :
    list=extract_filter(position_x,position_y)
    x=pd.DataFrame(list)
    x.columns=['X','Y']
    #Cluster K-means
    model=KMeans(n_clusters=8)
    model.fit(x)
    number_now=model.labels_[0]
    for number in range(len(model.labels_)) :
        if number_now!=model.labels_[number] :
            if distance_between_two_point(list[number-1][0],list[number-1][1],list[number][0],list[number][1])<10 :
                for s in range(len(model.labels_)):
                    if model.labels_[s]==model.labels_[number]:
                        model.labels_[s]=number_now
            else :
                number_now=model.labels_[number]
                        
    colormap=np.array(['Red','green','blue','yellow',"cyan","black","magenta","purple"])
    plt.scatter(x.X, x.Y,c=colormap[model.labels_],s=40)
    plt.title('The last hope')
    plt.xlabel('x')
    plt.ylabel('y')
    
    plt.show()
    number_now=model.labels_[0]
    list_info=[]
    list_in=[]
    for i in range(len(model.labels_)) :
        if model.labels_[i]!=number_now :
            list_info.append(list_in)
            list_in=[]
            list_in.append(list[i])
            number_now=model.labels_[i]
        else :
            list_in.append(list[i])
    list_info.append(list_in)
    return_list=[]       
    global distance_to_remove_the_tower,position_tower_x,position_tower_y
    for m in range(len(list_info)) :
        if len(list_info[m])!=0 :
            u,v=the_point_structure(list_info[m],position_x,position_y)
            plt.scatter(u,v)
            if distance_between_two_point(u,v,position_tower_x,position_tower_y)>distance_to_remove_the_tower:#remove the huge tower
                return_list.append([u,v])
    plt.scatter(position_x,position_y,color="r")
    print(temps.time()-start)
    
    return return_list

print(main_look(0,0))