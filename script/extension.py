import sqlite3
from datetime import datetime, timedelta
import json
from openpyxl import load_workbook 
import calendar

def found_index(sheet,column_count,apertura_biblio):
    for i in range(3,column_count+1):
        if sheet.cell(row=1, column=i).value==apertura_biblio:
            return i
    return column_count


def select_aula(nome_biblio,apertura_biblio="09:00",chiusura_biblio="18:00"):
    giorno=calendar.day_name[datetime.now().weekday()]
    #nome_biblio='bsi'
    try:
        wb = load_workbook('excel/'+ nome_biblio +'/settimana_'+ nome_biblio +'.xlsx') 
        sheet = wb[giorno] 
    except:
        print("errore apertura file, o il file non esite o non esiste il giorno")
        return "N/A"

    row_count = sheet.max_row 
    column_count = sheet.max_column 

    data = datetime.strptime(str(datetime.now())[11:16], '%H:%M')
    #data=datetime.strptime("14:12", '%H:%M') #for testing

    index_apertura=found_index(sheet,column_count,apertura_biblio)
    index_chiusura=found_index(sheet,column_count,chiusura_biblio)
    for i in range(index_apertura,index_chiusura):
        val = datetime.strptime(sheet.cell(row=1, column=i).value, '%H:%M')
        if val > data:
            orario=i-1
            break

    diz={}
    for i in range(2, row_count): 
        diz[i]=0
        
        for j in range(orario, index_chiusura): 
            val = sheet.cell(row=i, column=j).value 
            if val is None:
                diz[i]=diz[i]+1
            else:
                break #aula occupata dall'orario necessario per l'apertura
    print(diz.items())
    ris=0 #number of free time slot
    best_row=0
    best_cap=0
    for key,value in diz.items():
        capacity=sheet.cell(row=key, column=2).value
        if (value==ris and capacity>best_cap and value!=0) or value>ris :
            ris=value
            best_row=key
            best_cap=capacity

    print(str(ris)+" "+ str(best_cap)+ " "+ str(best_row))
    if ris<4: #mettere ris<4 cosi che le aule le si pare per almeno un'ora
        print("non ci sono aule disponibili per estendere la biblioteca")
        return "N/A"
    else:
        apertura=sheet.cell(row=1, column=orario).value
        chiusura=sheet.cell(row=1, column=orario+ris).value
        nome_aula=sheet.cell(row=best_row, column=1).value
        print("apro aula " + nome_aula + " con capienza : " + str(best_cap) + " dalle " + apertura + " alle " + chiusura )
        return nome_aula,best_cap,apertura,chiusura

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

def extend_biblio(nome_biblio, fascia_oraria):

    aula, capienza, apertura, chiusura=select_aula(nome_biblio, fascia_oraria[0:5], fascia_oraria[6:])
    diz = { 
        "name" : aula,
        "capacity" : capienza,
        "open_from" : apertura,
        "open_until" : chiusura
    }
    update_db("biblioteche", f"extension = ('{json.dumps(diz)}')", f"nome = '{nome_biblio}'", "../tessere.db")
    update_db("biblioteche", "is_extended = 1", f"nome = '{nome_biblio}'", "../tessere.db")
    
def close_biblio(nome_biblio):
    update_db("biblioteche", f"extension = ('closed')", f"nome = '{nome_biblio}'", "../tessere.db")
    update_db("biblioteche", "is_extended = 0", f"nome = '{nome_biblio}'", "../tessere.db")

def main():
    biblioteche = collect_biblioteche()

    
        
    
    for biblioteca in biblioteche:
        nome = biblioteca[0]
        count = biblioteca[1]
        capienza = biblioteca[2]
        is_extended = biblioteca[3]
        opening_hours=json.loads(biblioteca[5])
        print(opening_hours)
        soglia = capienza - count
        #print(nome + str(soglia) + str(is_extended))

        if is_extended == True:
            extension = json.loads(biblioteca[4])
            if datetime.strptime(extension["open_until"], "%H:%M") < datetime.strptime(str(datetime.now())[11:16], '%H:%M'):
                print("Sto chiudendo la biblio " + nome)
                close_biblio(nome)
        
        if soglia <= 2 and is_extended == False:
            if opening_hours[calendar.day_name[datetime.now().weekday()]] =="N/A":
                continue
            print("Sto estendendo la biblio " + nome)
            extend_biblio(nome, opening_hours[calendar.day_name[datetime.now().weekday()]])

            




if __name__ == "__main__":
    main()