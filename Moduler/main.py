#########################################
# Main program module for ACM9000       #
# By Simon Erlandsson & Gustav Burman   #
#                                       #
# Version 2.1:2018-04-25                #
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
#   TODO:
# - Logg for images and position etc
# - Check that units are consitent
# - Optimize for performance
# - Major cleanup
# - Setup code where user puts the step motor in the middle 90 degrees
# (- Implement a degree lock so the motor can't turn more than 180 degrees) Do we really want this?
##########################################

class positionlogg():
    def __init__(self):
        ###########
        #CONSTANTS#
        ###########
        self.gearratio=5                                                    #Transmission constant
        self.motor_steprevolution=200                                       #Number of steps per revolution for the motor only
        self.steprevolution=self.motor_steprevolution*self.gearratio        #Number of steps per revolution
        self.degreelock=180                                                 #How many degrees the motor should be able to turn
        self.camerawidth=112                                                #!!!This should be assigned with/based on camera.resoution!!!
        self.cameraFOV=62                                                   #Camera Field Of View (degrees)
        self.cameraFOV_steps=round(self.cameraFOV/360*self.steprevolution)  #Camera Field Of View measured in steps
        self.steplock=self.degreelock/360*self.steprevolution               #How many steps the motor should be able to turn

        #TODO: Setup code here where user puts the step motor in the middle 90 degrees
        #################
        #POSITION VALUES#
        #################
        self.COV = self.steprevolution//4                                   #Current Center Of View (Position from left border position to center of view)
        self.errorvalue=0                                                   #Where the measured value is compared to the last image taken (image position)
        self.imageposition=self.steprevolution//4                           #Where the latest images was taken
        #######
        #OTHER#
        #######
        self.textlog=queue.Queue()                                          #Used to communicate messages to the main thread
        
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
    """This method starts two threads: the motor thread and the image processing thread"""
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
    try:
        positionlogg.textlog.put('Initializing motor module')
        H=Hbrygga()
        while loop:
            PosX = positionlogg.get_realerror() #In steps
            if PosX>10:
                positionlogg
                steps=PosX
                while steps>0:
                    H.onestep(0.02,True)
                    positionlogg.COV+=1
                    steps-=1
            elif PosX<-10:
                steps=abs(PosX)
                while steps>0:
                    H.onestep(0.02,False)
                    positionlogg.COV-=1
                    steps-=1
    except Exception as e:
        positionlogg.textlog.put(e)
        positionlogg.textlog.put('end')
def image_module(positionlogg):
    """Image module that takes care of taking images with the camera and processing it"""
    try:
        positionlogg.textlog.put('Initializing image module')
        camera=picamera.PiCamera()
        implementsettings(camera)
        while True:
            t0=time.time()
            image=takeRGBimage(camera).array
            t1=time.time()
            currentPos=positionlogg.COV #So we know where the image was taken
            t2=time.time()
            #positionlogg.textlog.put('Taking picture at ' + str(currentPos))
            im2=image.copy()
            t3=time.time()
            FiltIm=OldGreenFilt(im2,[100,210,100],10)
            t4=time.time()
            #positionlogg.textlog.put('Filtering')
            #misc.imsave('TestPic' +str(n)+'.jpeg', image)
            #misc.imsave('TestPicGreen' +str(n)+'.jpeg', FiltIm)
            #[PosX,PosY]=GreenPos(FiltIm)
            [PosX,PosY]=PosFunOneD(FiltIm)
            t5=time.time()
            #positionlogg.textlog.put('Position found: ' + str(PosX))
            if abs(PosX)>10:
                positionlogg.errorvalue=positionlogg.PixelsToSteps(PosX)
                positionlogg.imageposition=currentPos
            t6=time.time()
            #positionlogg.textlog.put(positionlogg.current_position())
            positionlogg.textlog.put('\ntakeRgbimage(camera).array: ' + str(t1-t0))
            positionlogg.textlog.put('currentPos=positionlogg.COV: ' + str(t2-t1))
            positionlogg.textlog.put('image.copy(): ' + str(t3-t2))
            positionlogg.textlog.put('GreenFilt: ' + str(t4-t3))
            positionlogg.textlog.put('PosFunOneD: ' + str(t5-t4))
            positionlogg.textlog.put('if abs(PosX)>10: ' + str(t5-t6))
            raise Exception('I was planted!')
    except Exception as e:
        positionlogg.textlog.put(e)
        positionlogg.textlog.put('end')
###################################################################
    
if __name__=="__main__":
    print('Setting up log')
    pl=positionlogg()
    print('Setting up modules')
    init_threaded_modules()
    while True:
        if pl.textlog:
            msg=pl.textlog.get() #Message from other threads
            print(msg)
            if  msg=='!':
                #log the current position in a log file
                pass
            elif  msg=='end':
                #end the program
                break;

    
