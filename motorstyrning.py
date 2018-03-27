###################################################
# Kod för styrning av motor/motorer med en        #
# krets med L298N och en raspberry pi:s GPIO-pins.#
# Av: Simon Erlandsson                            #
# Version: 2.0:2018-03-27                         #
###################################################
import RPi.GPIO as GPIO
import time

#TODO:
#- Ensteg
#- Överföringfunktion (reglerfel -> antal steg + hastighet)
#- Hastighetsfunktion



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
        #GPIO.output(self.ctrlpins_list, GPIO.LOW)                # sets all to GPIO.LOW
        #GPIO.output(chan_list, (GPIO.HIGH, GPIO.LOW))   # sets first HIGH and second LOW
        try:
            while True:
                self.stepForward(1,0.01)
                GPIO.output(self.ctrlpins_list, self.state0)
        except KeyboardInterrupt:
            GPIO.cleanup() #Resets the status of any GPIO-pins (run before end)

    def stepForward(self, steps, s_delay):
        #Steps: antalet en-steg
        #s_delay: Hur många sekunder mellan varje steg
        for i in range(steps):
            self.nextState()
            time.sleep(s_delay)

    def nextState(self):
        if self.state==2:
            GPIO.output(self.ctrlpins_list, self.state1)
        elif self.state==3:
            GPIO.output(self.ctrlpins_list, self.state2)
        elif self.state==0:
            GPIO.output(self.ctrlpins_list, self.state3)
        else: #self.state==4
            GPIO.output(self.ctrlpins_list, self.state3)
        self.state=(self.state + 1)%4
    def stepBackward(self, steps, s_delay):
        pass
    def prevousState(self):
        pass
    def setupState(self):
        """Går igenom all states på motor och sätter state till start-state"""
        speed=0.01 #
        
        GPIO.output(self.ctrlpins_list, self.state1)
        time.sleep(speed)
        GPIO.output(self.ctrlpins_list, self.state0)
        time.sleep(speed)
        GPIO.output(self.ctrlpins_list, self.state2)
        time.sleep(speed)
        GPIO.output(self.ctrlpins_list, self.state0)
        time.sleep(speed)
        GPIO.output(self.ctrlpins_list, self.state3)
        time.sleep(speed)
        GPIO.output(self.ctrlpins_list, self.state0)
        time.sleep(speed)
        GPIO.output(self.ctrlpins_list, self.state4)
        time.sleep(speed)
        GPIO.output(self.ctrlpins_list, self.state0)
        time.sleep(speed)
        
        self.state=0

if __name__=="__main__":
    Hb=Hbrygga()
    Hb.loop()
    
