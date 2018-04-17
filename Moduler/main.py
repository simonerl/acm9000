#########################################
# Main program module for ACM9000       #
# By Simon Erlandsson & Gustav Burman   #
#                                       #
# Version 1.0:2018-04-17                #
#########################################
# This program will connect the different
# modules for the ACM9000 project
#########################################
import threads

class positionlogg():
    def __init__():
        ###########
        #CONSTANTS#
        ###########
        self.steprevolution=200 #Number of steps per revolution
        self.degreelock=180 #How many degrees the motor should be able to turn
        self.camerawidth= #!!!This should be assigned with/based on camera.resoution!!!
        self.cameraFOV=67#!!!SHOW THAT THIS IS THE CASE!!! #Camera Field Of View
        self.cameraFOV_steps=self.cameraFOV//360*self.steprevolution #Camera Field Of View measured in steps
        self.cameraFOV_steps=self.cameraFOV//360*self.camerawidth #Camera Field Of View measured in pixels
        self.steplock=self.degreelock/360*self.steprevolution #How many steps the motor should be able to turn

        #TODO: Setup code here where user puts the step motor in the middle 90 degrees (or 50 steps)

        self.position = self.steprevolution//4 #Position where the camera is currenly turned
        self.refposition = self.steprevolution//4 #Reference position where the camera should be
        self.errorvalue=self.position - self.refposition #Where the reference value is compared to the measured value
    def set_position(imstartposition_pixel, imcenterposition_pixel)
        """Sets the self.position value based on image startpoint and image center point"""
        
