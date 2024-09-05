from issuer import Issuer
from menu import Menu
from pointofsale import PointOfSale
from rfid import RFID
from keypad import Keypad

host_url = "https://localhost:3001"
terminal_id = 9003

currency = 'R'
card_value = ''
card_amount = ''
buffer = ''
blockingFlag = False
menu = Menu()
pos = PointOfSale()
print(pos.current_state)
issuer = Issuer(host_url)
keypad = Keypad()
rfid = RFID()

def read(character):
    global buffer
    match character:
        case '*' | 'A' | 'B' | 'C' | 'D':
            buffer = ''
            menu.standby(currency)
        case '#':
            print(buffer)
            card_amount = buffer
            buffer = ''
            menu.awaitingCard(currency, card_amount)
            pos.switchToRead()
        case _:
            buffer = buffer + str(character)
            print(character)
            menu.writeString(character)

def readCancel(character):
    global buffer
    global blockingFlag
    match character:
        case '*':
            pos.switchToStandby()
            menu.standby(currency)
            blockingFlag = True
try:
    while True:
        if pos.startUpState.is_active:
            symbol = issuer.getDetails(terminal_id)
            currency = symbol
            menu.initialize()
            menu.standby(currency)
            pos.switchFromInit()
        if pos.standbyState.is_active:
            keypad.read(read)
            # pos.switchToRead()
        if pos.readState.is_active:
            id = rfid.read()
            while not id:
                keypad.read(readCancel)
                if blockingFlag: 
                    break
                id = rfid.read()
                if id:
                    card_value = id
                    pos.switchToProcess()
        if pos.processState.is_active:
            menu.connecting()
            menu.authorizing(card_value)
            result = issuer.postTransaction(card_amount, card_value, terminal_id)
            menu.result(result)
            menu.standby(currency)
            pos.switchBackToStandby()
except KeyboardInterrupt:
    menu.clearScreen()
    keypad.cleanup()
    print("\nApplication stopped!")