###################################################
# Kod för styrning av motor/motorer med en        #
# krets med L298N och en raspberry pi:s GPIO-pins.#
# Av: Simon Erlandsson                            #
# Version: 2.0:2018-03-27                         #
###################################################


class Hbrygga:
    def __init__(self):
        pass
    def setup(self):
        import RPi.GPIO as GPIO
        import time
        
        #setup GPIO using Board numbering
        GPIO.setmode(GPIO.BOARD)
        
        #Controller GPIO-pins: 31 33 35 37
        #Enabling pins: 36 38

        #Setting up outputs:
        self.ctrlpins_list = [31,33,35,37]
        self.enblpins_list = [36,38]
        GPIO.setup(ctrlpins_list, GPIO.OUT)
        GPIO.setup(enblpins_list, GPIO.OUT, initial=GPIO.HIGH)

        self.state0=(GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW) #Idle
        self.state1=(GPIO.HIGH, GPIO.LOW, GPIO.HIGH, GPIO.LOW)
        self.state2=(GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH)
        self.state3=(GPIO.LOW, GPIO.HIGH,GPIO.LOW, GPIO.HIGH)
        self.state4=(GPIO.LOW, GPIO.HIGH,GPIO.HIGH, GPIO.LOW)
    def loop(self):
        #GPIO.output(self.ctrlpins_list, GPIO.LOW)                # sets all to GPIO.LOW
        #GPIO.output(chan_list, (GPIO.HIGH, GPIO.LOW))   # sets first HIGH and second LOW
        while True:
            stepForward(1,0.1)
    def stepForward(self,steps, s_delay):
        #Steps: antalet fyra-steg
        #ms_delay: Hur många sekunder mellan varje steg
        for i in range(steps):
            GPIO.output(self.ctrlpins_list, self.state1)
            time.sleep(s_delay)
            GPIO.output(self.ctrlpins_list, self.state2)
            time.sleep(s_delay)
            GPIO.output(self.ctrlpins_list, self.state3)
            time.sleep(s_delay)
            GPIO.output(self.ctrlpins_list, self.state4)
            time.sleep(s_delay)
        pass
    def nextState(self):
        pass
    def stepBackward(self, steps, s_delay):
        pass
    def prevousState(self):
        pass

if __name__=="__main__":
    Hb=Hbrygga()
    Hb.setup()
    Hb.loop()
    GPIO.cleanup() #Resets the status of any GPIO-pins (run before end)
