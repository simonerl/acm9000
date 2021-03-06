###################################################
# Code for driving a motor with a cicuitry        #
# containing L298N and a Raspberry Pi's GPIO-pins.#
# By: Simon Erlandsson                            #
# Version: 2.3:2018-05-14                         #
###################################################
import RPi.GPIO as GPIO
import time

class Hbrygga:
    def __init__(self):
        #setup GPIO using Board numbering
        GPIO.setmode(GPIO.BOARD)
        
        #Controller GPIO-pins: 31 33 35 37
        #Enabling pins: 36 38 

        #Setting up outputs:
        self.ctrlpins_list = [31,33,35,37]
        GPIO.setup(self.ctrlpins_list, GPIO.OUT)


        #HIGH = 3 V
        #LOW = 
        self.state0=(GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW) #Idle
        self.state1=(GPIO.HIGH, GPIO.LOW, GPIO.HIGH, GPIO.LOW)
        self.state2=(GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH)
        self.state3=(GPIO.LOW, GPIO.HIGH,GPIO.LOW, GPIO.HIGH)
        self.state4=(GPIO.LOW, GPIO.HIGH,GPIO.HIGH, GPIO.LOW)
        self.setupState()
    def loop(self):
        """Main-loop for stepping"""
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
        """Takes a number of steps, and sleeps for s_delay seconds, clockwise or anti-clockwise"""
        #Steps: number of steps
        #s_delay: How many second between each step
        for i in range(steps):
            self.nextState(turnclockwise)
            time.sleep(s_delay)

    def onestep(self, s_delay, turnclockwise):
        """Takes a step, and sleeps for s_delay seconds"""

        self.nextState(turnclockwise)
        time.sleep(s_delay)

    def nextState(self, turnclockwise):
        """Sets the next state on the motor based on if it's moving clockwise or anti-clockwise"""
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
            
    def setToIdle(self):
        """Lets the motor rest so it doesn't get to hot"""
        GPIO.output(self.ctrlpins_list, self.state0)
    def setupState(self):
        """Goes through all states on the motor and sets it to the starting state"""
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
            
if __name__=="__main__":
    Hb=Hbrygga()
    Hb.loop()
    
