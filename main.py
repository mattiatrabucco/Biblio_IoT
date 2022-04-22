import serial
import sqlite3


con = sqlite3.connect('tessere.db')
cur = con.cursor()
tessere = []
for row in cur.execute('SELECT id_tessera FROM tessere_unimore'):
    tessere.append(row[0])
con.close()
print(tessere)


#s = serial.Serial('COM3') #WINDOWS
s = serial.Serial('/dev/tty.usbmodem101') #MACOS
while True:
    res = s.readline()
    res = res.decode("utf-8")[:-2]
    tornello = res[7]
    print(res)
    #print(tornello)
    if "Card UID" in res:
        id_letto = res[-11:]

        if tornello == '0': #INGRESSO
            print(id_letto)
            if id_letto in tessere: #se è una tessera unimore
                tessere_current = []

                con = sqlite3.connect('tessere.db')
                cur = con.cursor()
                for row in cur.execute('SELECT id_tessera FROM biblio_ingmo_current'): #salvo tutti gli id attualmente dentro la biblio
                    tessere_current.append(row[0])
                
                if id_letto not in tessere_current: #se non già dentro
                    print("OK")
                    s.write(b"OK\n")

                    # Insert a row of data
                    cur.execute("INSERT INTO biblio_ingmo_current VALUES ('" + id_letto + "')")

                    # Save (commit) the changes
                    con.commit()
                else:
                    print("ERROR: sei gia' dentro")
                    s.write(b"ERROR: sei gia' dentro\n")
            else:
                print("ERROR: non puoi entrare")
                s.write(b"ERROR: non puoi entrare\n")
    con.close()
