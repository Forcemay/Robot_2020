class Drop_area() :
    def __init__(self) :
        self.state="active"
        self.x=1800
        self.list_position=[[1750,270-25,"green"],[1750,270-50,"green"],[1750,270+25,"red"],[1750,270+50,"red"],[1800,270-25,"green"],[1800,270-50,"green"],[1800,270+25,"red"],[1800,270+50,"red"],[1850,270-25,"green"],[1850,270-50,"green"],[1850,270+25,"red"],[1850,270+50,"red"],[1940,270-25,"green"],[1940,270-50,"green"],[1940,270+25,"red"],[1940,270+50,"red"]]#list of red withtout the farest last [y,angle,color]
    

            
    def ask(self) :
        if self.state=="active" :
            info=self.list_position.pop()
            if len(self.list_position)==0 :
                self.state="un_active"
            return info
            
        else :
            return ["%","%","%"]
    
drop_area=Drop_area()
import time

while drop_area.state=="active":
    print(drop_area.ask())
print(drop_area.state)