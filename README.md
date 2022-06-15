# Biblio IoT


## Introduzione

Biblio IoT è un sistema per ottimizzare l'uso delle biblioteche universitarie usando un microcontrollore **[Arduino](https://www.arduino.cc/)**, **[Django](https://www.djangoproject.com/)**, **[Minze](https://minze.dev/)** e **[Telegram](https://telegram.org/)**.

Il prototipo realizzato simula un tornello per l'accesso ad una biblioteca. Tramite API RESTful e supporto cloud-based fornisce una dashboard pubblica sullo stato delle varie strutture universitarie e un bot Telegram. Permette inoltre l'espansione in aulee adiacenti. 

## Requisiti

```
pyserial
django
python-decouple
openpyxl
pyTelegramBotAPI
djangorestframework
```


## Arduino

Il dispositivo relizzato con Arduino usa: 
- N°2 RFID-RC522
- N°1 Display LCD
- N°2 LED

per simulare un tornello per l'accesso ad una biblioteca.
