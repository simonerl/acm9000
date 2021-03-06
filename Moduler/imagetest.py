#########################################
# Test program for camera and           #
# imageprocessing.                      #
# By Simon Erlandsson & Gustav Burman   #
#                                       #
# Version 2.1:2018-05-14                #
#########################################
from imageshooter import *
from imageprocessing import *
from PIL import *
import time

#Functions used for data writing to file
def writelines(name, matrix):
    """Adds a matrix of values to a file by the name of '(name).dat'"""
    with open(name+'.dat', 'a') as file:
        for row in matrix:
            rowtext=str(row[0])
            for i in range(1,len(row)):
                rowtext += ',' + str(row[i])
            file.write(rowtext + '\n')
def emptyfile(name):
    """Empties the filem stated as '(name).dat'"""
    open(name+'.dat', 'w').close() 
if __name__ == "__main__":
    camera=picamera.PiCamera()
    implementsettings(camera)
    emptyfile('testdata') #Remember to save file after every re-run
    num=1
    
    #Setup for position function
    print('Setup for GreenPos')
    columns=int(input('Columns (112|224): '))
    rows=int(input('Rows (80|160): '))
    print(str(columns),str(rows))
    
    camera.resolution=(columns,rows)
    MultMatrix=np.transpose(np.zeros(columns))
    b=0
    while b <= columns:
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
        
        FiltIm=SuperGreenFilt(im2)
        t4=time.time()
        #[PosX,PosY]=PosFunOneD(FiltIm[:,:,1]) "Not interested in this one
        #PosY2=0;
        PosX=GreenPos(FiltIm[:,:,1],MultMatrix,rows,columns) #Rename
        t5=time.time()
        if abs(PosX)>10:
            print('WITHIN 10 PIXELS. NO NEW POSITION ASSIGNED')
        t6=time.time()


        
        #Saving images:
        FiltIm[:,int(PosX+columns/2-1)]=127 #Draws a line at PosX
        print('PosX is ' + str(PosX))
        misc.imsave('/media/pi/USB DISK/TESTBILDER/testi'+str(num)+'.jpg', image)
        misc.imsave('/media/pi/USB DISK/TESTBILDER/testg'+str(num)+'.jpg', FiltIm)

        #Printing the time it took to do each step
        print('\ntakeRgbimage(camera).array: ' + str(t1-t0))
        print('image.copy(): ' + str(t3-t1))
        print('GreenFilt: ' + str(t4-t3))
        print('PosFunOneD: ' + str(t5-t4))
        print('if abs(PosX)>10: ' + str(t5-t6))
        writelines('testdata',[[num,avstand,PosX, t1-t0,t3-t1,t4-t3,t5-t4,t6-t5]])

        num+=1

