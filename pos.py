from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
from statemachine import StateMachine, State
import requests
import os

class Menu:
    def initialize(self):
        lcd.clear()
        lcd.write_string('Connecting to network')
        time.sleep(2)
        lcd.clear()
        lcd.write_string('Fetching configuration')
        time.sleep(2)
        lcd.clear()
        lcd.write_string('Ready')
        time.sleep(2)

    def standby(self):
        lcd.clear()
        lcd.write_string('Sandbox Pay\r\nEnter Amount:\r\n' + currency)

    def connecting(self):
        lcd.clear()
        lcd.write_string("Initializing connection")
        time.sleep(2)
        lcd.clear()
        lcd.write_string("Connected")
        time.sleep(2)

    def authorizing(self):
        lcd.clear()
        lcd.write_string("Authorizing: " + str(card_value))
        time.sleep(2)
    def result(self, result):
        lcd.clear()
        if result:
            lcd.write_string("Transaction Successful")
        else:
            lcd.write_string("Transaction Declined")
        time.sleep(2)

    def awaitingCard(self):
        lcd.clear()
        lcd.write_string("Amount to Pay:\r\n" + currency + str(card_amount) +"\r\n\r\nPresent Card...")

# need to establish a connection to the yet to be built card provider
# this would fetch the mcc code that this machine is working under
# would then go into a standby state waiting for the amount to be put in
# once the amount has been put in the pound # must be pressed
# it will then go into nfc read mode * to cancel
# if cancelled, go back to amount screen
# if card received. card number and amount is sent to card provider
# response from card provider is to be displayed on the screen
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=20, rows=4, dotsize=8)
menu = Menu()
currency = 'R'
card_value = ''
card_amount = ''

class PointOfSale(StateMachine):
 
    # creating states
    startUpState = State("startup", initial = True)
    standbyState = State("standby")
    readState = State("read")
    processState = State("process")
      
    # transitions of the state
    switchFromInit = startUpState.to(standbyState)
    switchToRead = standbyState.to(readState)
    switchToStandby = readState.to(standbyState)
    switchToProcess = readState.to(processState)
    switchBackToStandby = processState.to(standbyState)
         
pos = PointOfSale()
print(pos.current_state)
# pos.switchToRead()
# print(pos.current_state)
# these GPIO pins are connected to the keypad
# change these according to your connections!

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

    def readLine(self, line, characters):
        GPIO.output(line, GPIO.HIGH)
        if(GPIO.input(self.C1) == 1):
            self.writeBuffer(characters[0])
        if(GPIO.input(self.C2) == 1):
            self.writeBuffer(characters[1])
        if(GPIO.input(self.C3) == 1):
            self.writeBuffer(characters[2])
        if(GPIO.input(self.C4) == 1):
            self.writeBuffer(characters[3])
        GPIO.output(line, GPIO.LOW)

    def read(self):
        # call the readLine function for each row of the keypad
        self.readLine(self.L1, ["1","2","3","A"])
        self.readLine(self.L2, ["4","5","6","B"])
        self.readLine(self.L3, ["7","8","9","C"])
        self.readLine(self.L4, ["*","0","#","D"])
        time.sleep(0.2)

    def writeBuffer(self, character):
        match character:
            case 'A':
                Shutdown()
            case '*':
                self.buffer = ''
                menu.standby()
            case '#':
                print(self.buffer)
                global card_amount
                card_amount = self.buffer
                self.buffer = ''
                menu.awaitingCard()
                pos.switchToRead()
            case _:
                self.buffer = self.buffer + str(character)
                print(character)
                lcd.write_string(character)
        
def readRfid():
        id, text = rfid.read()
        if id != "":
            global card_value
            card_value = id
            pos.switchToProcess()
            print(card_value)
        # print(id)
        # print(text)

def getDetails():
    # The API endpoint to communicate with
    url = "http://192.168.1.170:3000/" + str(9004)

    # A GET request to tthe API
    response = requests.get(url)

    # Print the response
    response_json = response.json()
    global currency
    currency = response_json["symbol"]
    print(response_json)

def postTransaction():
    print(card_value)
    new_data = {
        "centsAmount": str(card_amount)+'00',
        "card": str(card_value),
        "terminalId": 9004
    }

    # The API endpoint to communicate with
    url_post = "http://192.168.1.170:3000/transaction"

    # A POST request to tthe API
    post_response = requests.post(url_post, json=new_data)

    # Print the response
    post_response_json = post_response.json()
    print(post_response_json)
    return post_response_json["result"]

def Shutdown():  
    os.system("sudo shutdown -h now") 

keypad = Keypad()

rfid = SimpleMFRC522()
try:
    while True:
        if pos.startUpState.is_active:
            getDetails()
            menu.initialize()
            menu.standby()
            pos.switchFromInit()
        if pos.standbyState.is_active:
            keypad.read()
            # pos.switchToRead()
        if pos.readState.is_active:
            readRfid()
        if pos.processState.is_active:
            menu.connecting()
            menu.authorizing()
            result = postTransaction()
            menu.result(result)
            menu.standby()
            pos.switchBackToStandby()
except KeyboardInterrupt:
    lcd.clear()
    GPIO.cleanup()
    print("\nApplication stopped!")