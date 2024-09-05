import RPi.GPIO as GPIO
import time

class Keypad():
    buffer = ''
    L1 = 6
    L2 = 13
    L3 = 19
    L4 = 26

    C1 = 12
    C2 = 16
    C3 = 20
    C4 = 21

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.L1, GPIO.OUT)
        GPIO.setup(self.L2, GPIO.OUT)
        GPIO.setup(self.L3, GPIO.OUT)
        GPIO.setup(self.L4, GPIO.OUT)

        # Make sure to configure the input pins to use the internal pull-down resistors

        GPIO.setup(self.C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # The readLine function implements the procedure discussed in the article
    # It sends out a single pulse to one of the rows of the keypad
    # and then checks each column for changes
    # If it detects a change, the user pressed the button that connects the given l>
    # to the detected column

    def readLine(self, line, characters, readFunc):
        GPIO.output(line, GPIO.HIGH)
        if(GPIO.input(self.C1) == 1):
            readFunc(characters[0])
        if(GPIO.input(self.C2) == 1):
            readFunc(characters[1])
        if(GPIO.input(self.C3) == 1):
            readFunc(characters[2])
        if(GPIO.input(self.C4) == 1):
            readFunc(characters[3])
        GPIO.output(line, GPIO.LOW)

    def read(self, readFunc):
        # call the readLine function for each row of the keypad
        self.readLine(self.L1, ["1","2","3","A"], readFunc)
        self.readLine(self.L2, ["4","5","6","B"], readFunc)
        self.readLine(self.L3, ["7","8","9","C"], readFunc)
        self.readLine(self.L4, ["*","0","#","D"], readFunc)
        time.sleep(0.2)

    def cleanup(self):
        GPIO.cleanup()