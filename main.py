import serial
import sqlite3

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

def insert_in_bibliomo(value):
    insert_in_db("biblio_ingmo_current", value, "tessere.db")

def setup_serial_connection():
    # ----- WINDOWS -----
    #return serial.Serial('COM3')

    # -----  MACOS  -----
    return serial.Serial('/dev/tty.usbmodem1101')

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

            if NFCreader_id == '0': # GOING IN
                
                #print(card_id)
                
                if card_id in authorized_cards: # If it's an authorized Unimore card
                    
                    current_cards = collect_current_cards()

                    if card_id not in current_cards: # If it's not already inside
                        print("OK: authorized card can enter")
                        arduino_serial.write(b"OK\n")

                        insert_in_bibliomo(card_id)

                    else:
                        print("ERROR: authorized card already inside")
                        arduino_serial.write(b"ERROR: already inside\n") 

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