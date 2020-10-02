import pump_principal
import Slide_principal

class Grab_brain_principal():
    def __init__(self):
        self.order="%"
        self.state="ini"

    def which_state(self) :
        if self.state=="ini":
            self.ini()
        elif self.state=="down_pump" :
            self.down_pump()
        elif self.state=="up" :
            self.up()

    def ini(self):
        if self.order="down_pump":
            self.action(-1,1)
            self.state="down_pump"

    def down_pump(self):
        if self.order="up" :
            self.action(1, 1)
            self.state = "up"

    def up(self):
        if self.order="ini":
            self.action(1, -1)
            self.state = "ini"

    def action(self,slide,pump):
        global slide,pump


