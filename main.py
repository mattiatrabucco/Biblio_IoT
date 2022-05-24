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

def collect_authorized_cards():
    return select_from_db("id_tessera", "tessere_unimore", "tessere.db")

def collect_current_cards():
    return select_from_db("id_tessera", "biblio_ingmo_current", "tessere.db")

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
    insert_in_db("biblio_ingmo_current", card_id, "tessere.db")
    log_insert(card_id)

# BE CAREFUL: NOT SAFE FROM SQL INJECTION!
def del_from_db(table, column, value, db_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    t = (value,)
    cur.execute(f"DELETE FROM {table} WHERE {column} = (?)", t)
    
    con.commit()
    con.close()

def remove_from_bibliomo(card_id):
    del_from_db("biblio_ingmo_current", "id_tessera", card_id, "tessere.db")
    log_remove(card_id)

def setup_serial_connection():
    # ----- WINDOWS -----
    #return serial.Serial('COM3')

    # -----  MACOS  -----
    return serial.Serial('/dev/tty.usbmodem1101')

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

def main_loop(authorized_cards, arduino_serial):
    
    while True:
        
        #TODO: Sanitize input!
        line_from_serial = arduino_serial.readline()
        line_from_serial = line_from_serial.decode("utf-8")[:-2]
        NFCreader_id = line_from_serial[7] # 0 --> GOING IN, 1 --> GOING OUT
        
        print(line_from_serial)
        #print(NFCreader_id)

        if "Card UID" in line_from_serial: # If the Arduino has read a card
            
            card_id = line_from_serial[-11:]

            if card_id in authorized_cards: # If it's an authorized Unimore card
                #print(card_id)

                # GOING IN 
                if NFCreader_id == '0':    
                    cards_already_inside = collect_current_cards()

                    if card_id not in cards_already_inside: # If it's not already inside

                        if update_counter(True):
                            print("OK: authorized card can enter")
                            arduino_serial.write(b"OK\n")
                            insert_in_bibliomo(card_id)
                        else:
                            print("ERROR: biblio full")
                            arduino_serial.write(b"ERROR: full\n") 

                    else:
                        print("ERROR: authorized card already inside")
                        arduino_serial.write(b"ERROR: already inside\n") 
                
                # GOING OUT
                elif NFCreader_id == '1': 
                    cards_already_inside = collect_current_cards()

                    if card_id in cards_already_inside: # If it's inside

                        if update_counter(False):
                            print("OK: authorized card can exit")
                            arduino_serial.write(b"OK\n")
                            remove_from_bibliomo(card_id)
                        else:
                            print("ERROR: db error")
                            arduino_serial.write(b"ERROR: db\n") 
                        

                    else:
                        print("ERROR: authorized card not inside")
                        arduino_serial.write(b"ERROR: not inside\n") 
                
                # ERROR
                else:
                    print("READER ERROR")

            else:
                print("ERROR: not authorized card")
                arduino_serial.write(b"ERROR: not authorized\n")    


def main():
    authorized_cards = collect_authorized_cards()
    
    print(authorized_cards)

    arduino_serial = setup_serial_connection()

    main_loop(authorized_cards, arduino_serial)



if __name__ == "__main__":
    main()