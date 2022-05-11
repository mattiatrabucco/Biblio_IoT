import sqlite3
from datetime import datetime
import json

# BE CAREFUL: NOT SAFE FROM SQL INJECTION!
def select_from_db(what, table, db_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    
    rows = []
    for row in cur.execute(f"SELECT {what} FROM {table}"):
        rows.append(row)
    
    con.close()
    return rows

def collect_biblioteche():
    return select_from_db("*", "biblioteche", "../tessere.db")

# BE CAREFUL: NOT SAFE FROM SQL INJECTION!
def update_db(table, value, condition, db_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    #cur.execute(f"UPDATE biblioteche SET is_extended = 1 WHERE nome = 'ingmo'")
    cur.execute(f"UPDATE {table} SET {value} WHERE {condition}")
    
    con.commit()
    con.close()

def extend_biblio(nome_biblio):

    diz = { 
        "name" : "P05",
        "capacity" : 30,
        "open_until" : str(datetime.now())
    }
    update_db("biblioteche", f"extension = ('{json.dumps(diz)}')", f"nome = '{nome_biblio}'", "../tessere.db")
    update_db("biblioteche", "is_extended = 1", f"nome = '{nome_biblio}'", "../tessere.db")
    

def main():
    biblioteche = collect_biblioteche()
    
    for biblioteca in biblioteche:
        nome = biblioteca[0]
        count = biblioteca[1]
        capienza = biblioteca[2]
        is_extended = biblioteca[3]

        soglia = capienza - count
        #print(nome + str(soglia) + str(is_extended))

        if soglia <= 2 and is_extended == False:
            print("Sto estendendo la biblio " + nome)
            extend_biblio(nome)
            




if __name__ == "__main__":
    main()