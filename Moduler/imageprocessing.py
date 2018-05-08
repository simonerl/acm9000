#########################################
# Filtering and image processing        #
# functions for ACM9000 project.        #
# By Simon Erlandsson & Gustav Burman   #
#                                       #
# Version 2.3:2018-05-08                #
#########################################

import numpy as np
from scipy import misc
import  time

def OldGreenFilt(RGB,REF,DivFactor):
        """This method does the same thing as GreenFilt but 100 times slower."""

        [m,k]=RGB.shape[0:2]
        #RGB=DivFactor*np.round(RGB/DivFactor)
        for i in range(0,m):                
                for j in range(0,k):
                        if RGB[i,j,1]<REF[1]*0.9:
                                RGB[i,j,:]=0 
                        elif RGB[i,j,1]/(RGB[i,j,0]+1) < 1 or RGB[i,j,1]/(RGB[i,j,2]+1)<1:
                                RGB[i,j,:]=0 
                        elif RGB[i,j,2]/(RGB[i,j,1]+1)>1.8*REF[2]/(REF[1]+1) or RGB[i,j,0]/(RGB[i,j,1]+1)>1.8*REF[0]/REF[1]:
                                RGB[i,j,:]=0                 
        return RGB[:,:,1]

def GreenFilt(RGB,REF):
        """Filters out everything but the color value intervalls given in REF. Returns a black and white (boolean) matrix."""
        #Källa: https://stackoverflow.com/questions/7722519/fast-rgb-thresholding-in-python-possibly-some-smart-opencv-code
        #Write REF in this way [(Rmin,Rmax),(Gmin,Gmax),(Bmin,Bmax)]
        #ex. [(90,130),(60,150),(50,210)]
        #[(0,100),(180,255),(0,100)]
        
        red_range = np.logical_and(REF[0][0] <= RGB[:,:,0], RGB[:,:,0] <= REF[0][1])
        green_range = np.logical_and(REF[1][0] <= RGB[:,:,1], RGB[:,:,1] <= REF[1][1])
        blue_range = np.logical_and(REF[2][0] <= RGB[:,:,2], RGB[:,:,2] <= REF[2][1])
        valid_range = np.logical_and(red_range, green_range, blue_range)

        RGB[valid_range] = 255                  #Output color value if true (all channels)
        RGB[np.logical_not(valid_range)] = 0    #Black if false
        return RGB
def SuperGreenFilt(RGB):
        """Filters out everything but green. Returns a black and white (boolean) matrix."""
        range1=np.logical_and(RGB[:,:,1] >= 121,RGB[:,:,1]>RGB[:,:,0])
        range2=np.logical_and(RGB[:,:,1]>RGB[:,:,2],RGB[:,:,0]<90,RGB[:,:,0]<80)
        valid_range=np.logical_and(range1,range2)
        RGB[valid_range] = 255                  #Output color value if true (all channels)
        RGB[np.logical_not(valid_range)] = 0    #Black if false
        return RGB

def GreenPos(RGB):
        """Finds the green mean-value of the image. Both X and Y axes."""
        #Can this be done faster with numpy logical gates?
        [m,k]=RGB.shape[0:2]
        GPos=np.int64(np.array([0,0]))
        for i in range(0,m):                
                for j in range(0,k):
                        GPos=(GPos+(RGB[i,j]*np.array([i,j])))  
        Pos=np.around(GPos/np.sum(RGB))
        return (int(Pos[0]),int(Pos[1]))

def PosFunOneD(RGB):
        """Finds the green center point with a smarter algorithm than GreenPos. X axis only."""
        [r,k]=RGB.shape[0:2]
        OneD=[] 
        for i in range(0,k):
                OneD.append(sum(RGB[:,i]))
        i=0
        while not OneD[i]:
                i+=1
                if i == k-1:
                        return (0,0)
        j=i
        while OneD[j]:
                j+=1
                if j == k-1:
                        return (0,0)
                
        Pos=i+(j-i)/2-k/2
        return (Pos,0)

def xxXtr3m3Sup3rGr33nPosXxx(FiltIm,MultMatrix,rows,columns):
        try:
                print(np.sum(FiltIm*MultMatrix))
                print(np.sum(FiltIm))
                ans=round(np.sum(FiltIm*MultMatrix)/float(np.sum(FiltIm)))
        except(Exception): #If NaN
                ans = 0
        return ans

def ProcessImage(RGB, REF):
        """Does all image procesing. BOth filtering and finding the right position and returns it"""
        FiltIm=OldGreenFilt(im2,[100,210,100],10)
        [PosX,PosY]=PosFunOneD(FiltIm)
        return PosX



if __name__=="__main__":
        #For testing purposes
        #import matplotlib.pyplot as plt
        import PIL as Image
        from imageshooter import *
        #img = misc.imread("test.jpeg")#image2.jpg test.jpeg
        camera=picamera.PiCamera()
        implementsettings(camera)
        
        arr = takeRGBimage(camera).array
        RGB=arr.copy()
        [i,j]=arr.shape[0:2]
        REF=[100,200,100]


        #Gim=GreenFilt(RGB,[(0,100),(180,255),(0,100)])
        Gim=SuperGreenFilt(RGB)

        #Pos=GreenPos(Gim[:,:,1])

        #Gim[Pos]=[255,0,0]
        #print(Pos)
        
        misc.imsave("test.jpeg",Gim)



	

