from mfrc522 import SimpleMFRC522

class RFID:  
    def __init__(self):
        self.rfid = SimpleMFRC522()
    def read(self):
        return self.rfid.read_id_no_block()
        # while not id:
        #     id = self.rfid.read_id_no_block()
        #     if id:
        #         return id
        # print(id)
