#Testing numpy
import time
from PIL import Image
import numpy as np
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
img = Image.open("baestfalseuvp.jpeg").convert('RGB')
arr = np.array(np.asarray(img))
arr2=arr.copy()
print(arr)
t0=time.time()
FiltIm=GreenFilt(arr2,[100,210,100],10)
t1=time.time()

R = [(90,130),(60,150),(50,210)]
red_range = np.logical_and(R[0][0] < arr[:,:,0], arr[:,:,0] < R[0][1])
green_range = np.logical_and(R[1][0] < arr[:,:,0], arr[:,:,0] < R[1][1])
blue_range = np.logical_and(R[2][0] < arr[:,:,0], arr[:,:,0] < R[2][1])
valid_range = np.logical_and(red_range, green_range, blue_range)

arr[valid_range] = 200
arr[np.logical_not(valid_range)] = 0
t2=time.time()

print('Numpy logical gates:',t2-t1)
print('Gamla GreenFilt:',t1-t0)
outim = Image.fromarray(arr)
outim2 = Image.fromarray(FiltIm)
outim.save("baestout.jpg")
outim2.save("baestout2.jpg")






