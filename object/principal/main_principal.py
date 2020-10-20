import random
import sys
from threading import Thread
import time
from ihm_robot import *

from pump_principal import *
from Slide_principal import *
from motor_principal import *
from Grab_brain_principal import *
from Drop_brain_principal import *
from Brain_principal import *

class Runner1(Thread):

    """Thread chargé simplement d'afficher une lettre dans la console."""

    def __init__(self, object):
        Thread.__init__(self)
        self.object = object

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        while 1:
            self.object.which_state()

class Runner2(Thread):

    """Thread chargé simplement d'afficher une lettre dans la console."""

    def __init__(self, object):
        Thread.__init__(self)
        self.object = object

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        while 1:
            which_state_global()
def which_state_global():
    l = [brain, drop_brain_principal, grab_brain_principal, slide1, slide2, pump1, pump2, pump3, pump4,pump5]
    for s in l:
        s.which_state()



Runner_list=["thread_1","thread_2"]
Runner_list[0] = Runner1(motors)
Runner_list[1] = Runner2(brain)

brain.flag=True
start_time=time.time()


for thread in Runner_list :
    thread.start()

for thread in Runner_list :
    thread.join()

