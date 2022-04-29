# Biblioteca IoT


TODO:

main.py
- [x] GOING IN
- [x] GOING OUT
- [ ] DB refactoring: single connect
- [ ] DB refactoring: log functions
- [ ] Sanitize some input (line 62)
- [ ] Insert/remove functions must be more generic to allow a portable code (e.g. using DEFINEs)
- [ ] Testing
- [ ] Create python directory

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
- [x] Login/Register user
- [x] Registration controllare campo null
- [x] Registration controllare campo mail che sia unimore
- [x] Registration controllare campo esadecimale card_id  -->CREATO FUNZIONE MAGARI OTTIMIZZABILE
- [x] Login non funziona con utenti diversi da django admin
- [x] Logout
- [ ] Salting password
- [x] Secret key exposed (now .env var)
- [x] Homepage con link a registrati 
- [x] Homepage con link a login
- [x] View con login solo per admin con relativa pagina html
- [ ] Funzionalita' pagina admin di visualizzare, aggiungere e rimuovere utenti (quando rimuovi un utente va rimosso da entrambe le tabelle sia utenti sia tessere_unimore)
- [ ] UX
- [x] Login con username unimore e non con mail