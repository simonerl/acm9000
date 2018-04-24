#########################################
# Filtering and image processing        #
# functions for ACM9000 project.        #
# By Simon Erlandsson & Gustav Burman   #
#                                       #
# Version 2.0:2018-04-24                #
#########################################
# This file is an altered version of KEXFUN.py
# - Cleaned up to be able to run on a RPi
# - Major cleanups to fit modularization
#########################################
import numpy as np
from scipy import misc
#import matplotlib.pyplot as plt
#import PIL as Image

def GreenFilt(RGB,REF,DivFactor):
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

def GreenPos(RGB): #En ide är att lägga in denna funktionalitet i Greenfilt för  att inte göra massa dubbelt arbete
        [m,k]=RGB.shape[0:2]
        GPos=np.int64(np.array([0,0]))
        for i in range(0,m):                
                for j in range(0,k):
                        GPos=(GPos+(RGB[i,j]*np.array([i,j])))  
        Pos=np.around(GPos/np.sum(RGB))
        return (int(Pos[0]),int(Pos[1]))
def PosFunOneD(RGB):
        [r,k]=RGB.shape[0:2]
        OneD=[] 
        for i in range(0,k):
                OneD.append(sum(RGB[:,i]))
        i=0
        j=k-1
        print(OneD)
        while not OneD[i]:
                i+=1
                if i == k:
                        return (0,0)
        j=i
        while OneD[j]:
                j+=1
                if j == r:
                        return (0,0)
                
        Pos=i+(j-i)/2-k/2
        return (Pos,0)
                
                
##img = misc.imread("test.jpeg")#image2.jpg test.jpeg
##
##arr = np.array(img)
##[i,j]=arr.shape[0:2]
##REF=[100,200,100]
##DivFactor=10;
##
##Gim=GreenFilt(arr,REF,DivFactor)
##
##Pos=GreenPos(Gim[:,:,1])
##
##Gim[Pos]=[255,0,0]
##print(Pos)
##
##from matplotlib import pyplot as plt
##plt.imshow(Gim, interpolation='nearest')
##plt.show()



	

