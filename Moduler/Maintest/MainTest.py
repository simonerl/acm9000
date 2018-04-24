import picamera
import picamera.array
import RPi.GPIO as GPIO
import time
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
        return RGB

def GreenPos(RGB): #En ide är att lägga in denna funktionalitet i Greenfilt för  att inte göra massa dubbelt arbete
        [m,k]=RGB.shape[0:2]
        GPos=np.int64(np.array([0,0]))
        for i in range(0,m):                
                for j in range(0,k):
                        GPos=(GPos+(RGB[i,j,1]*np.array([i,j])))  
        Pos=np.around(GPos/np.sum(RGB))
        try:
            return (int(Pos[0]),int(Pos[1]))
        except:
            return False

def implementsettings(camera):
    """Will implement the settings below for a picamera object"""
    camera.sensor_mode=0 #Automatiskt av resolution och framerate
    camera.resolution= (112, 80)
    camera.sharpness = 0
    camera.contrast = 0
    camera.brightness = 50
    camera.saturation = 0
    camera.ISO = 50
    camera.video_stabilization = False
    camera.exposure_compensation = 0
    camera.exposure_mode = 'sports'
    camera.meter_mode = 'average'
    camera.awb_mode = 'auto'
    camera.image_effect = 'none'
    camera.color_effects = None
    camera.rotation = 0
    camera.hflip = True
    camera.vflip = True
    camera.crop = (0.0, 0.0, 1.0, 1.0)
    camera.image_denoise=False

def takeRGBimage(camera):
    """Takes an images and returns an RGB matrix in the form of a picamera.array.PiRGBArray"""
    output=picamera.array.PiRGBArray(camera)
    output.truncate(0)
    #Specific for camera.capture:
    uvp = True # use_video_port  
    camera.capture(output, 'rgb',use_video_port=uvp)
    return output

class Hbrygga:
    def __init__(self):
        #setup GPIO using Board numbering
        GPIO.setmode(GPIO.BOARD)
        
        #Controller GPIO-pins: 31 33 35 37
        #Enabling pins: 36 38 

        #Setting up outputs:
        self.ctrlpins_list = [31,33,35,37]
        #self.enblpins_list = [36,38] #Ger bara 3V
        GPIO.setup(self.ctrlpins_list, GPIO.OUT)
        #GPIO.setup(self.enblpins_list, GPIO.OUT, initial=GPIO.HIGH)

        #HIGH = 3 V
        #LOW = 
        self.state0=(GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW) #Idle
        self.state1=(GPIO.HIGH, GPIO.LOW, GPIO.HIGH, GPIO.LOW)
        self.state2=(GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH)
        self.state3=(GPIO.LOW, GPIO.HIGH,GPIO.LOW, GPIO.HIGH)
        self.state4=(GPIO.LOW, GPIO.HIGH,GPIO.HIGH, GPIO.LOW)
        #GPIO.setwarnings(False) #Use to disable warnings.
        self.setupState()
    def loop(self):
        """Main-loop för stegning"""
        #GPIO.output(self.ctrlpins_list, GPIO.LOW)                # sets all to GPIO.LOW
        #GPIO.output(chan_list, (GPIO.HIGH, GPIO.LOW))   # sets first HIGH and second LOW
        try:
            while True:
                self.velocityFunction(100, True)
                self.velocityFunction(100, False)
                #self.step(100,0.005, True)
                #self.step(100,0.1, False)
                #GPIO.output(self.ctrlpins_list, self.state0)
        except KeyboardInterrupt:
            GPIO.cleanup() #Resets the status of any GPIO-pins (run before end)

    def step(self, steps, s_delay, turnclockwise):
        """Ta ett antal steg, med s_delay mellan varje steg, med eller mot klockan"""
        #Steps: antalet en-steg
        #s_delay: Hur många sekunder mellan varje steg
        for i in range(steps):
            self.nextState(turnclockwise)
            time.sleep(s_delay)

    def nextState(self, turnclockwise):
        """Sätter nästa state på motorn beroende på om den ska röra sig med eller mot klockan"""
        if self.state==0:
            GPIO.output(self.ctrlpins_list, self.state1)
        elif self.state==1:
            GPIO.output(self.ctrlpins_list, self.state2)
        elif self.state==2:
            GPIO.output(self.ctrlpins_list, self.state3)
        else: #self.state==3
            GPIO.output(self.ctrlpins_list, self.state4)
        if turnclockwise==True: #clockwise
            self.state=(self.state + 1)%4
        else: #anti-clockwise
            self.state=(self.state - 1)%4

    def setupState(self):
        """Går igenom all states på motor och sätter state till start-state"""
        speed=0.01 #
        
        GPIO.output(self.ctrlpins_list, self.state1)
        time.sleep(speed)
        GPIO.output(self.ctrlpins_list, self.state2)
        time.sleep(speed)
        GPIO.output(self.ctrlpins_list, self.state3)
        time.sleep(speed)
        GPIO.output(self.ctrlpins_list, self.state4)
        time.sleep(speed)
        
        self.state=0
        
    def velocityFunction(self, steps,turnclockwise):
        s_delay=lambda stepscount: 1/(steps-steps_count)
        steps_count=0
        for i in range(steps):
            self.nextState(turnclockwise)
            time.sleep(s_delay(steps_count))
            steps_count+=1

camera=picamera.PiCamera()
implementsettings(camera)
H=Hbrygga()
n=0;
while True:
<<<<<<< HEAD:Moduler/MainTest.py
    image=takeRGBimage(camera)
    FiltIm=GreenFilt(image)
    [PosX,PosY]=GreenPos(FiltIm)
    if PosX<112/2:
        H.step(10,20,True)
    elif PosX>112/2:
        H.step(10,20,False)
=======
    t1=time.time()
    n+=1;
    image=takeRGBimage(camera).array
    im2=image.copy()
    t2=time.time()
    print('Taking an imagetakes: '+str(t2-t1))
    t3=time.time()
    FiltIm=GreenFilt(im2,[100,210,100],10)
    t4=time.time()
    t43=t4-t3
    print('The GreenFilt takes: '+ str(t43))
    #misc.imsave('TestPic' +str(n)+'.jpeg', image)
    #misc.imsave('TestPicGreen' +str(n)+'.jpeg', FiltIm)
    t5=time.time()
    Pos=GreenPos(FiltIm)
    t6=time.time()
    t65=t6-t5
    print( 'The GreenPos takes: ' + str(t65))
    if not Pos:
        print("Im sorry Dave,im afraid i cant do that..")
    else:
        [PosY,PosX]=Pos
        print(PosX,PosY)
        print(im2.shape)
        if PosX<112/4:
            H.step(30,0.01,False)
            print("Stepping Right")
        else:
            H.step(30,0.01,True)
            print("Stepping Left")
        t7=time.time()
        t=t7-t1
        print('Calculation time was: ' + str(t))
##    H.step(3000,0.01,False)
##    H.step(3000,0.01,True)
    
    
>>>>>>> f275448d0b2cb2c1850fa18190d3294714466c22:Moduler/Maintest/MainTest.py
        
    
















    
