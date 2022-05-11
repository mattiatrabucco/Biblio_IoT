# Biblioteca IoT


TODO:

main.py
- [ ] DB refactoring: single connect
- [ ] DB refactoring: log functions
- [ ] Sanitize some input (line 62)
- [ ] Insert/remove functions must be more generic to allow a portable code (e.g. using DEFINEs)
- [ ] Testing
- [ ] Create python directory
- [x] GOING IN
- [x] GOING OUT

script.py
- [ ] Script to clean DB 

Biblio_IoT.ino
- [ ] Testing
- [ ] Delay tuning
- [ ] Create arduino directory

DB
- [x] Tabella counter
- [x] Tabella log
- [x] Add mail column in Tessere

DJANGO
- [ ] AULA ESTESA
- [ ] Integrazione orario aule su excel
- [ ] Funzionalita' pagina admin di visualizzare, aggiungere e rimuovere utenti (quando rimuovi un utente va rimosso da entrambe le tabelle sia utenti sia tessere_unimore e per ora da problemi la rimozione da tessere_unimore)
- [ ] Visualizzare "closed" per una biblioteca fuori dagli orari di apertura
- [ ] Previsione futura tipo: "Next hour will be more crowded"
- [ ] Confronto con la stessa settimana nel passato tipo: "Today has about the same crowds as last week"
- [ ] Mostrare le ore di punta tipo: "Peak hours are 6pm, 7pm, and 8pm"
- [x] Visualizzare capienza biblio
- [x] Completare funzione/algoritmo where_to_go --> definire priorità e considerazioni che deve fare
- [ ] UX
- [x] Modificare tabella tessere e togliere password --> pensare tipo a campo booleano is_registered
- [x] Login/Register user
- [x] Registration controllare campo is None
- [x] Registration controllare campo mail che sia unimore
- [x] Registration controllare campo esadecimale card_id 
- [x] Login non funziona con utenti diversi da django admin
- [x] Logout
- [x] Secret key exposed (now .env var)
- [x] Homepage con link a registrati 
- [x] Homepage con link a login
- [x] View con login solo per admin con relativa pagina html
- [x] Login con username unimore e non con mail