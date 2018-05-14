#########################################
# Main program module for ACM9000       #
# By Simon Erlandsson & Gustav Burman   #
#                                       #
# Version 2.4:2018-05-14                #
#########################################
# This program connects the different
# modules for the ACM9000 project
#########################################

import threading
from imageshooter import *
from motorstyrning import *
from imageprocessing import *
import queue


class positionlog():
    def __init__(self):
        ###########
        #CONSTANTS#
        ###########
        self.gearratio=5                                                    #Transmission constant
        self.motor_steprevolution=200                                       #Number of steps per revolution for the motor only
        self.steprevolution=self.motor_steprevolution*self.gearratio        #Number of steps per revolution
        self.camerawidth=112                                                
        self.cameraheight=80                                                
        self.cameraFOV=62                                                   #Camera Field Of View (degrees)
        self.cameraFOV_steps=round(self.cameraFOV/360*self.steprevolution)  #Camera Field Of View measured in steps

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
    
    def PixelsToSteps(self,pixels):
        """Transforms image pixels to step motor steps"""
        steps= round(pixels/self.camerawidth*self.cameraFOV_steps)
        return int(steps)
    
    def get_realerror(self):
        """Returns the error value of the current position"""
        return self.imageposition+self.errorvalue-self.COV
    
    def __str__(self):
        """Return the current position values"""
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
       
def motor_module(positionlog,loop=True):
    """Motor module that runs the motor on a thread"""
    try:
        positionlog.textlog.put('Initializing motor module')
        H=Hbrygga()
        while loop:
            PosX = positionlog.get_realerror() #In steps
            if PosX>10:
                positionlog
                H.onestep(0.018,True)
                positionlog.COV+=1
            elif PosX<-10:
                H.onestep(0.018,False)
                positionlog.COV-=1
            else:
                H.setToIdle() #Let the motor rest so it doesn't get to hot
    except Exception as e:
        positionlog.textlog.put(e)
        positionlog.textlog.put('end')
def image_module(positionlog):
    """Image module that takes care of taking images with the camera and processing it"""
    try:
        positionlogg.textlog.put('Initializing image module')
        camera=picamera.PiCamera()
        implementsettings(camera)

        #Setup for position function
        columns=int(positionlog.camerawidth)
        rows=int(positionlog.cameraheight)
        MultMatrix=np.transpose(np.zeros(columns))
        b=0
        while b <= columns:
            MultMatrix[b]=b-columns/2+1;
            b+=1
        while True:
            image=takeRGBimage(camera).array
            currentPos=positionlog.COV #So we know where the image was taken
            im2=image.copy()
            FiltIm=GreenFilt(im2)
            PosX=GreenPos(FiltIm[:,:,1],MultMatrix,rows,columns)
            step_PosX=positionlog.PixelsToSteps(PosX)
            
            if abs(step_PosX) > 10: #If position is to small don't save the data
                positionlog.errorvalue=step_PosX
                positionlog.imageposition=currentPos
                
            positionlog.textlog.put('Step position: ' + str(step_PosX))

    except Exception as e:
        positionlog.textlog.put(e)
        positionlog.textlog.put('end')
###################################################################
    
if __name__=="__main__":
    print('Setting up log')
    pl=positionlog()
    print('Setting up modules')
    init_threaded_modules()
    while True:
        if pl.textlog:
            msg=pl.textlog.get() #Message from other threads
            print(msg)
            if  msg=='end':
                print('A thread crashed. Shutting down...')
                #end the program
                break;
    H=Hbrygga()
    H.setToIdle()
    
