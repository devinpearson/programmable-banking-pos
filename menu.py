import time
from RPLCD.i2c import CharLCD

class Menu:

    def __init__(self):
        self.lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=20, rows=4, dotsize=8)

    def initialize(self):
        self.lcd.clear()
        self.lcd.write_string('Connecting to\r\nnetwork')
        time.sleep(2)
        self.lcd.clear()
        self.lcd.write_string('Fetching\r\nconfiguration')
        time.sleep(2)
        self.lcd.clear()
        self.lcd.write_string('Ready')
        time.sleep(2)

    def standby(self, symbol):
        self.lcd.clear()
        self.lcd.write_string('Sandbox Pay\r\nEnter Amount:\r\n' + symbol)

    def connecting(self):
        self.lcd.clear()
        self.lcd.write_string("Initializing\r\nconnection")
        time.sleep(2)
        self.lcd.clear()
        self.lcd.write_string("Connected")
        time.sleep(2)

    def authorizing(self, value):
        self.lcd.clear()
        self.lcd.write_string("Authorizing: " + str(value))
        time.sleep(2)
    def result(self, result):
        self.lcd.clear()
        if result:
            self.lcd.write_string("Transaction\r\nSuccessful")
        else:
            self.lcd.write_string("Transaction\r\nDeclined")
        time.sleep(6)

    def awaitingCard(self, symbol, value):
        self.lcd.clear()
        self.lcd.write_string("Amount to Pay:\r\n" + symbol + str(value) +"\r\n\r\nPresent Card...")
    
    def writeString(self, character):
        self.lcd.write_string(character)

    def clearScreen(self):
        self.lcd.clear()