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
#import queue

#########################################
#TODO: Logg for images and position etc

class positionlogg():
    def __init__(self):
        ###########
        #CONSTANTS#
        ###########
        #TODO: Change settings so it fits with the transmission
        self.steprevolution=200 #Number of steps per revolution
        self.degreelock=180 #How many degrees the motor should be able to turn
        self.camerawidth= 0 #!!!This should be assigned with/based on camera.resoution!!!
        self.cameraFOV=67#!!!SHOW THAT THIS IS THE CASE!!! #Camera Field Of View (degrees)
        self.cameraFOV_steps=self.cameraFOV//360*self.steprevolution #Camera Field Of View measured in steps
        self.cameraFOV_pixels=self.cameraFOV//360*self.camerawidth #Camera Field Of View measured in pixels
        self.steplock=self.degreelock/360*self.steprevolution #How many steps the motor should be able to turn

        #TODO: Setup code here where user puts the step motor in the middle 90 degrees (or 50 steps)
        #################
        #POSITION VALUES#
        #################
        self.COV = self.steprevolution//4 #Current Center Of View (Position from left border position to center of view)
        self.errorvalue=0 #Where the measured value is compared to the current COV
        
    def add_steps(self,steps):
        """Adding steps the motor has moved: positive to the right, negative to the left"""
        #TODO:
        # - Make this thread-secured
        # - Implement so the motor can't turn more than degreelock
        self.COV += steps
        self.errorvalue-=steps #This might write as the same time as image_module(!!!) 
        
    
def init_threaded_modules():
    #New motor module thread 
    motorThread=threading.Thread(target = motor_module, args=(pl,True))
    motorThread.daemon=False #Will termiate when main-thread ends
    motorThread.start()
    #New image module thread 
    motorThread=threading.Thread(target = image_module, args=(pl))
    motorThread.daemon=False #Will termiate when main-thread ends
    motorThread.start()
    
###################################################
#TODO: Modules must be MORE prefabricated. They should come i already packed functions. Think modularization... 
###################################################
def motor_module(positionlogg,loop=True):
    """Motor module that runs the motor on a thread"""
    H=Hbrygga()
    while loop:
        time.sleep(10)
        PosX = positionlogg.errorvalue
        print('PosX:',PosX)
        #TODO: add number of steps moved to logg
        if not PosX:
            print("Im sorry Dave,im afraid i cant do that..")
        else:
            if PosX<112/4:
                H.step(30,0.01,False)
                print("Stepping Right")
            else:
                H.step(30,0.01,True)
                print("Stepping Left")
                
def image_module(positionlogg):
    """Image module that takes care of taking images with the camera and processing it"""
    camera=picamera.PiCamera()
    implementsettings(camera)
    while True:
        image=takeRGBimage(camera).array
        currentPos=positionlogg.position #So we know where the image was taken
        im2=image.copy()
        FiltIm=GreenFilt(im2,[100,210,100],10)
        #misc.imsave('TestPic' +str(n)+'.jpeg', image)
        #misc.imsave('TestPicGreen' +str(n)+'.jpeg', FiltIm)
        [PosX,PosY]=GreenPos(FiltIm)
        positionlogg.errorvalue=PosX

###################################################################
    
if __name__=="__main__":
    print('Setting up logg')
    pl=positionlogg()
    print('Setting up modules')
    init_threaded_modules()
    while True:
        time.sleep(1000)
    
