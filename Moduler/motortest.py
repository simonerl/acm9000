#########################################
# Test program for motor control        #
# By Simon Erlandsson & Gustav Burman   #
#                                       #
# Version 1.0:2018-05-08                #
#########################################
from motorstyrning import *

def motor_module(speed,loop=True):
    """Motor module that runs the motor on a thread"""
    try:
        H=Hbrygga()
        while loop:
            if speed > 0:
                H.onestep(speed,True)
            elif speed < 0:
                H.onestep(abs(speed),False)
            else:
                H.setToIdle() #Let the motor rest so it doesn't get to hot
    except Exception as e:
        positionlogg.textlog.put(e)
        positionlogg.textlog.put('end')
class Speed():
    def __init__(self):
        self.speed=0
    def update(self, SPEED):
        self.speed=SPEED
        
s=Speed()

#New motor module thread 
motorThread=threading.Thread(target = motor_module, args=(s,True))
motorThread.daemon=True #Will termiate when main-thread ends
motorThread.start()

while True:
    i=float(input('New speed: '))
    s.update(i)
