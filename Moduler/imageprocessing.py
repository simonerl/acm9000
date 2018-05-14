#########################################
# Filtering and image processing        #
# functions for ACM9000 project.        #
# By Simon Erlandsson & Gustav Burman   #
#                                       #
# Version 2.4:2018-05-14                #
#########################################

import numpy as np
from scipy import misc
import  time

def GreenFilt(RGB):
        """Filters out everything but green. Returns a black and white (boolean) matrix."""
        range1=np.logical_and(RGB[:,:,1] >= 121,RGB[:,:,1]>RGB[:,:,0])
        range2=np.logical_and(RGB[:,:,1]>RGB[:,:,2],RGB[:,:,0]<90,RGB[:,:,2]<80)
        valid_range=np.logical_and(range1,range2)
        RGB[valid_range] = 255                  #Output color value if true (all channels)
        RGB[np.logical_not(valid_range)] = 0    #Black if false
        return RGB

def GreenPos(FiltIm,MultMatrix,rows,columns):
        """Finds the green mean-value of the image. X axis only."""
        a=np.sum(FiltIm*MultMatrix)
        b=np.sum(FiltIm)
        if b == 0:
                ans=0
        else:
                ans=round(a/b)
        return ans

if __name__=="__main__":
        
        #For testing purposes
        import PIL as Image
        from imageshooter import *
        camera=picamera.PiCamera()
        implementsettings(camera)
        
        arr = takeRGBimage(camera).array
        RGB=arr.copy()

        Gim=GreenFilt(RGB)
        
        misc.imsave("test.jpeg",Gim)



	

