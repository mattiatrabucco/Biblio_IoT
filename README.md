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
- [ ] Login/Register user
- [ ] Registration controllare campo null
- [ ] Registration controllare campo mail che sia unimore
- [ ] Registration controllare campo esadecimale card_id
- [ ] Login non funziona con utenti diversi da django admin
- [ ] Logout
- [ ] Salting password
- [ ] Secret key exposed (https://stackoverflow.com/questions/64208678/hiding-secret-key-in-django-project-on-github-after-uploading-project)
- [ ] Homepage con link a registrati e login
- [ ] Layout admin add user page
- [ ] UX