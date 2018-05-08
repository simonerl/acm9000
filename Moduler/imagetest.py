#########################################
# Test program for camera and           #
# imageprocessing.                      #
# By Simon Erlandsson & Gustav Burman   #
#                                       #
# Version 1.0:2018-05-07                #
#########################################
from imageshooter import *
from imageprocessing import *
from PIL import *
import time

#Functions used for data writing to file
def writelines(name, matrix):
    with open(name+'.dat', 'a') as file:
        for row in matrix:
            rowtext=str(row[0])
            for i in range(1,len(row)):
                rowtext += ',' + str(row[i])
            file.write(rowtext + '\n')
def emptyfile(name):
    open(name+'.dat', 'w').close() #Empty file

camera=picamera.PiCamera()
implementsettings(camera)
emptyfile('testdata')
num=1
#Setup for position function
print('Setup for GreenPos')
columns=int(112)
rows=int(80)
print(str(columns),str(rows))
MultMatrix=np.transpose(np.zeros(columns))
b=0
for v in MultMatrix:
    MultMatrix[b]=b-columns/2+1;
    b+=1
print(str(MultMatrix))
while True:
    
    avstand=input('At what distance is the object?')
    t0=time.time()
    image=takeRGBimage(camera).array
    t1=time.time()
    im2=image.copy()
    t3=time.time()
    
    #FiltIm=OldGreenFilt(im2,[100,210,100],10)
    #FiltIm=GreenFilt(im2,[(0,120),(150,255),(0,120)])
    FiltIm=SuperGreenFilt(im2)
    t4=time.time()
    [PosX,PosY]=PosFunOneD(FiltIm[:,:,1])
    PosY2=0;
    PosX2=xxXtr3m3Sup3rGr33nPosXxx(FiltIm[:,:,1],MultMatrix,rows,columns)
    
    t5=time.time()
    #positionlogg.textlog.put('Position found: ' + str(PosX))
    if abs(PosX)>10:
        print('WITHIN 10 PIXELS. NO NEW POSITION ASSIGNED')
    t6=time.time()
    #Saving images:
    FiltIm[:,int(PosX+55)]=127 #PosX är beräknat utifrånn mitten av bilden
    FiltIm[:,int(PosX2+55)]=200
    print(str(PosX))
    print(str(PosX2))
    misc.imsave('/media/pi/USB DISK/TESTBILDER/testi'+str(num)+'.jpg', image)
    misc.imsave('/media/pi/USB DISK/TESTBILDER/testg'+str(num)+'.jpg', FiltIm)
    num+=1
    print('\ntakeRgbimage(camera).array: ' + str(t1-t0))
    print('image.copy(): ' + str(t3-t1))
    print('GreenFilt: ' + str(t4-t3))
    print('PosFunOneD: ' + str(t5-t4))
    print('if abs(PosX)>10: ' + str(t5-t6))
    writelines('testdata',[[PosX,PosY, t1-t0,t3-t1,t4-t3,t5-t4, t6-t5, avstand]])
