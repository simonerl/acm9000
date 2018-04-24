#########################################
# Main program module for ACM9000       #
# By Simon Erlandsson & Gustav Burman   #
#                                       #
# Version 2.0:2018-04-24                #
#########################################
# This program will connect the different
# modules for the ACM9000 project
#########################################

import threading
from imageshooter import *
from motorstyrning import *
from imageprocessing import *
import time
import queue

#########################################
#TODO: Logg for images and position etc

class positionlogg():
    def __init__(self):
        ###########
        #CONSTANTS#
        ###########
        #TODO: Change settings so it fits with the transmission
        self.gearratio=5 #Transmission constant
        self.motor_steprevolution=200 #Number of steps per revolution for the motor only
        self.steprevolution=self.motor_steprevolution*self.gearratio #Number of steps per revolution
        self.degreelock=180 #How many degrees the motor should be able to turn
        self.camerawidth=112 #!!!This should be assigned with/based on camera.resoution!!!
        self.cameraFOV=62#!!!SHOW THAT THIS IS THE CASE!!! #Camera Field Of View (degrees)
        self.cameraFOV_steps=round(self.cameraFOV/360*self.steprevolution) #Camera Field Of View measured in steps
        self.steplock=self.degreelock/360*self.steprevolution #How many steps the motor should be able to turn

        #TODO: Setup code here where user puts the step motor in the middle 90 degrees
        #################
        #POSITION VALUES#
        #################
        self.COV = self.steprevolution//4 #Current Center Of View (Position from left border position to center of view)
        self.errorvalue=0 #Where the measured value is compared to the last image taken (image position)
        self.imageposition=self.steprevolution//4 # Where the latest images was taken
        #######
        #OTHER#
        #######
        self.textlog=queue.Queue()
        self.isTurning=False #is the motor turning. set this to false and the motor stops
    def add_steps(self,steps):
        """Adding steps the motor has moved: positive to the right, negative to the left"""
        #TODO:
        # - Make this thread-secured
        # - Implement so the motor can't turn more than degreelock
        self.COV += steps
        #self.errorvalue-=steps #This might write as the same time as image_module(!!!)
    def add_step(self):
        self.COV += 1
    def subtract_step(self):
        self.COV -= 1
    def DegreesToSteps(self,degree):
        steps=round(degree/360*self.steprevolution)
        return steps
    def StepsToDegrees(self,steps):
        degree=round(steps/self.steprevolution*360)
        
    def PixelsToSteps(self,pixels):
        steps= round(pixels/self.camerawidth*self.cameraFOV_steps)
        return int(steps)
    def get_realerror(self):
        return self.imageposition+self.errorvalue-self.COV #Error value from the current position
    def current_position(self):
        text='COV: ' + str(self.COV) +'\nerrorvalue: ' + str(self.errorvalue) + '\nimageposition: ' + str(self.imageposition) + '\nrealerror: ' + str(self.get_realerror())
        return text
def init_threaded_modules():
    #New motor module thread 
    motorThread=threading.Thread(target = motor_module, args=(pl,True))
    motorThread.daemon=True #Will termiate when main-thread ends
    motorThread.start()
    #New image module thread 
    imageThread=threading.Thread(target = image_module, args=(pl,))
    imageThread.daemon=True #Will termiate when main-thread ends
    imageThread.start()
    
###################################################
#TODO: Modules must be MORE prefabricated. They should come i already packed functions. Think modularization... 
###################################################
def motor_module(positionlogg,loop=True):
    """Motor module that runs the motor on a thread"""
    positionlogg.textlog.put('Initializing motor module')
    H=Hbrygga()
    while loop:
        PosX = positionlogg.get_realerror()
        if PosX>10:
            steps=positionlogg.PixelsToSteps(PosX)
            positionlogg.isTurning=True
            while positionlogg.isTurning and steps>0:
                H.onestep(0.01,True)
                positionlogg.COV+=1
                steps-=1
            positionlogg.isTurning=False
        elif PosX<-10:
            steps=abs(positionlogg.PixelsToSteps(PosX))
            positionlogg.isTurning=True
            while positionlogg.isTurning and steps>0:
                H.onestep(0.01,False)
                positionlogg.COV-=1
                steps-=1
            positionlogg.isTurning=False


                
def image_module(positionlogg):
    """Image module that takes care of taking images with the camera and processing it"""
    positionlogg.textlog.put('Initializing image module')
    camera=picamera.PiCamera()
    implementsettings(camera)
    while True:
        image=takeRGBimage(camera).array
        currentPos=positionlogg.COV #So we know where the image was taken
        #positionlogg.textlog.put('Taking picture at ' + str(currentPos))
        im2=image.copy()
        FiltIm=GreenFilt(im2,[100,210,100],10)
        #positionlogg.textlog.put('Filtering')
        #misc.imsave('TestPic' +str(n)+'.jpeg', image)
        #misc.imsave('TestPicGreen' +str(n)+'.jpeg', FiltIm)
        #[PosX,PosY]=GreenPos(FiltIm)
        [PosX,PosY]=PosFunOneD(FiltIm)
        #positionlogg.textlog.put('Position found: ' + str(PosX))
        if PosX:
            positionlogg.errorvalue=PosX
            positionlogg.imageposition=currentPos
            positionlogg.isTurning=False #STop the motor from turning
        positionlogg.textlog.put(positionlogg.current_position())

###################################################################
    
if __name__=="__main__":
    print('Setting up log')
    pl=positionlogg()
    print('Setting up modules')
    init_threaded_modules()
    while True:
        if pl.textlog:
            print(pl.textlog.get())
    
