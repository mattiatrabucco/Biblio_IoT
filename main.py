import requests
import serial
import sqlite3
from datetime import datetime

facolta='ingmo'
# BE CAREFUL: NOT SAFE FROM SQL INJECTION!
def select_from_db(what, table, db_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    
    rows = []
    for row in cur.execute(f"SELECT {what} FROM {table}"):
        rows.append(row[0])
    
    con.close()
    return rows

def collect_current_cards():
    return select_from_db("id_tessera", "presenze_attuali", f"{facolta}.db")

# BE CAREFUL: NOT SAFE FROM SQL INJECTION!
def insert_in_db(table, value, db_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    t = (value,)
    cur.execute(f"INSERT INTO {table} VALUES (?)", t)
    
    con.commit()
    con.close()

def log_insert(cardid):
    con = sqlite3.connect("tessere.db")
    cur = con.cursor()

    cur.execute("INSERT INTO log_unimo VALUES (?, ?, ?, ?)", (cardid, datetime.now(), "IN", facolta))
    
    con.commit()
    con.close()

def log_remove(cardid):
    con = sqlite3.connect("tessere.db")
    cur = con.cursor()

    cur.execute("INSERT INTO log_unimo VALUES (?, ?, ?, ?)", (cardid, datetime.now(), "OUT", facolta))
    
    con.commit()
    con.close()

def insert_in_bibliomo(card_id):
    insert_in_db("presenze_attuali", card_id, f"{facolta}.db")

# BE CAREFUL: NOT SAFE FROM SQL INJECTION!
def del_from_db(table, column, value, db_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    t = (value,)
    cur.execute(f"DELETE FROM {table} WHERE {column} = (?)", t)
    
    con.commit()
    con.close()

def remove_from_bibliomo(card_id):
    del_from_db("presenze_attuali", "id_tessera", card_id, f"{facolta}.db")

def setup_serial_connection():
    # ----- WINDOWS -----
    return serial.Serial('COM3')

# True = GOING IN, False = GOING OUT
def update_counter(mode):
    con = sqlite3.connect("tessere.db")
    cur = con.cursor()
    
    val = cur.execute("SELECT count, capienza FROM biblioteche WHERE nome='ingmo'")
    
    for v in val:
        val = v #eventualmente vedi next()

    count = val[0]
    capacity = val[1]

    if mode:
        #GOING IN
        if count >= capacity:
            #BIBLIO FULL
            return False
        count = count + 1
        
        cur.execute(f"UPDATE biblioteche SET count='{count}' WHERE nome='ingmo'")
    
        con.commit()
    else:
        #GOING OUT
        if count == 0:
            #DB ERROR!
            return False
        count = count - 1
        
        cur.execute(f"UPDATE biblioteche SET count='{count}' WHERE nome='ingmo'")
    
        con.commit()


    con.close()
    return True

class Bridge:
    def __init__(self):
        self.api_ip = '192.168.75.123:8000'
        self.api_version = 'api/v1'
        self.in_buffer = []
        self.arduino_serial = serial.Serial('/dev/tty.usbmodem1201') # -----  MACOS  -----
        self.is_inside = False
        self.auth_cards = []
        self.capacity=3
        self.counter=0

        response = requests.get(f'http://{self.api_ip}/{self.api_version}/all_auth_cards')
        if response.status_code == 200:
            print("API: list of cards loaded")
            self.auth_cards = response.json()['OK']
            print(self.auth_cards)
    
    def is_auth_card(self, card_id):
        if len(self.auth_cards) != 0:
            upd_card = ' '.join(card_id[i:i+2] for i in range(0, len(card_id), 2))
            return upd_card in self.auth_cards
        else:
            response = requests.get(f'http://{self.api_ip}/{self.api_version}/auth_card/{facolta}/{card_id}')
            if response.status_code == 200:
                print("API: card ok")
                self.is_inside = response.json()['OK']
                return True
            return False
    
    def read_card(self):
        card_id = b''.join(self.in_buffer[1:]).decode()
        upd_card = ' '.join(card_id[i:i+2] for i in range(0, len(card_id), 2))
        reader_id = self.in_buffer[0].decode()
        
        print(card_id)
        print(reader_id)
        
        if self.is_auth_card(card_id): # API request: check if it's an authorized Unimore card
            cur_card_list = collect_current_cards()
            print(cur_card_list)

            # GOING IN 
            if reader_id == '0':    
                #if not self.is_inside: # If it's not already inside
                if upd_card not in cur_card_list: # If it's not already inside
                    if self.counter < self.capacity:
                        self.arduino_serial.write(b"OK")
                        self.counter += 1
                        print("API OK: authorized card can enter")
                        insert_in_bibliomo(upd_card)
                        response = requests.post(f'http://{self.api_ip}/{self.api_version}/library/{facolta}/{card_id}/', json={"way":"IN"})
                    else:
                        self.arduino_serial.write(b"NO") 
                        print("ERROR: biblio full")

                else:
                    self.arduino_serial.write(b"NO") 
                    print("ERROR: authorized card already inside")
            
            # GOING OUT
            elif reader_id == '1': 
                #if self.is_inside: # If it's inside
                if upd_card in cur_card_list: # If it's inside

                    if self.counter > 0:
                        self.arduino_serial.write(b"OK")
                        self.counter -= 1
                        print("API OK: authorized card can exit")
                        remove_from_bibliomo(upd_card)
                        response = requests.post(f'http://{self.api_ip}/{self.api_version}/library/{facolta}/{card_id}/', json={"way":"OUT"})
                    else:
                        self.arduino_serial.write(b"NO") 
                        print("ERROR: db error")

                else:
                    self.arduino_serial.write(b"NO") 
                    print("ERROR: authorized card not inside")
            
            # ERROR
            else:
                print("READER ERROR")

        else:
            self.arduino_serial.write(b"NO")   
            print("ERROR: not authorized card")

    def loop(self):
        
        while True:
            if self.arduino_serial.in_waiting > 0:
                value = self.arduino_serial.read(1)
                if value == b'\xFF':
                    self.read_card()
                    self.in_buffer = []
                else:
                    self.in_buffer.append(value)


if __name__ == "__main__":
    

    my_bridge = Bridge()
    my_bridge.loop()